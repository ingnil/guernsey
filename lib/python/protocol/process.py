#
#    Guernsey - Library to simplify creating REST web services using Python and Twisted
#    Copyright (C) 2014 Magine Sweden AB
#    Copyright (C) 2016 Ingemar Nilsson
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# Currently, this module only provides two base classes for process protocols.
#

from twisted.internet import protocol, defer

import guernsey.util as util

import datetime
import logging

class LoggingProtocol(protocol.ProcessProtocol):
    def __init__(self, name):
        self._name = name
        self.__class__.logger = util.getLogger(self)

    def connectionMade(self):
        self.logger.debug("[%s] Connected to process", self._name)

    def outReceived(self, data):
        self.logger.debug("[%s] Received stdout data: '%s'", self._name, data)

    def errReceived(self, data):
        self.logger.debug("[%s] Received stderr data: '%s'", self._name, data)

    def inConnectionLost(self):
        self.logger.debug("[%s] In connection lost", self._name)

    def outConnectionLost(self):
        self.logger.debug("[%s] Out connection lost", self._name)

    def errConnectionLost(self):
        self.logger.debug("[%s] Err connection lost", self._name)

    def processExited(self, status):
        self.logger.debug("[%s] Process exited with status '%s'", self._name, status)

    def processEnded(self, status):
        self.logger.debug("[%s] Process ended with status '%s'", self._name, status)
        self.logger.debug("[%s] status.value.__dict__: %r", self._name, status.value.__dict__)


class Log(object):
    def __init__(self, maxSize=0):
        self.log = ""
        self.maxSize = maxSize

    def append(self, data):
        self.log += data
        if self.maxSize and len(self.log) > self.maxSize:
            self.log = self.log[-self.maxSize:]

    def __str__(self):
        return self.log


class CaptureOutputProtocol(LoggingProtocol):
    def __init__(self, name, deferred=defer.Deferred(), maxLogSize=0):
        LoggingProtocol.__init__(self, name)
        self.__deferred = deferred
        self.__stdoutLog = Log(maxLogSize)
        self.__stderrLog = Log(maxLogSize)
        self.__lastUpdated = datetime.datetime.utcnow()

    def getDeferred(self):
        return self.__deferred

    def outReceived(self, data):
        self.__stdoutLog.append(data)
        self.logger.debug("[%s] Appended stdout data to capture log: '%s'", self._name, data)
        self.__lastUpdated = datetime.datetime.utcnow()

    def errReceived(self, data):
        self.__stderrLog.append(data)
        self.logger.debug("[%s] Appended stderr data to capture log: '%s'", self._name, data)
        self.__lastUpdated = datetime.datetime.utcnow()

    def processEnded(self, reason):
        LoggingProtocol.processEnded(self, reason)
        self.__lastUpdated = datetime.datetime.utcnow()
        result = {
            "stdout": self.getStdout(),
            "stderr": self.getStderr(),
            "exitcode": reason.value.exitCode,
            "lastUpdated": self.__lastUpdated
            }
        if reason.value.exitCode == 0:
            self.getDeferred().callback(result)
        else:
            self.getDeferred().errback(result)

    def getStdout(self):
        return str(self.__stdoutLog).replace("\r", "\n").replace("\r\n", "\n")

    def getStderr(self):
        return str(self.__stderrLog).replace("\r", "\n").replace("\r\n", "\n")

    def getLastUpdated(self):
        return self.__lastUpdated

# Deprecated name for CaptureOutputProtocol
class CheckOutputProtocol(CaptureOutputProtocol):
    pass


class LineReceiverProtocol(LoggingProtocol):
    _pendingOut = None
    _pendingErr = None
    _outLines = None
    _errLines = None

    def __init__(self, name, deferred=None):
        LoggingProtocol.__init__(self, name)
        self._pendingOut = ""
        self._pendingErr = ""
        self._deferred = deferred
        self._outLines = []
        self._errLines = []

    def outLineReceived(self, line):
        self.logger.debug("[%s] Received stdout line: '%s'", self._name, line)
        if self._deferred:
            self._outLines.append(line)
        
    def errLineReceived(self, line):
        self.logger.debug("[%s] Received stderr line: '%s'", self._name, line)
        if self._deferred:
            self._errLines.append(line)

    def outReceived(self, data):
        dataToProcess = (self._pendingOut + data).replace("\r\n", "\n").replace("\r", "\n")
        lines = dataToProcess.split("\n")
        for line in lines[:-1]:
            self.outLineReceived(line)
        self._pendingOut = lines[-1]

    def errReceived(self, data):
        dataToProcess = (self._pendingErr + data).replace("\r\n", "\n").replace("\r", "\n")
        lines = dataToProcess.split("\n")
        for line in lines[:-1]:
            self.errLineReceived(line)
        self._pendingErr = lines[-1]

    def processEnded(self, reason):
        LoggingProtocol.processEnded(self, reason)
        if self._pendingOut:
            self.outLineReceived(self._pendingOut)
        if self._pendingErr:
            self.errLineReceived(self._pendingErr)

        if self._deferred:
            result = {
                "stdout": self._outLines,
                "stderr": self._errLines,
                "exitcode": reason.value.exitCode
            }
            if reason.value.exitCode == 0:
                self._deferred.callback(result)
            else:
                self._deferred.errback(result)


class FilteredLineReceiverProtocol(LineReceiverProtocol):
    _filterFunc = None
    _filterErr = None
    
    def __init__(self, name, filterFunc, filterErr=False, deferred=None):
        LineReceiverProtocol.__init__(self, name, deferred)
        self._filterFunc = filterFunc
        self._filterErr = filterErr

    def outFilteredLineReceived(self, line):
        self.logger.debug("[%s] Received filtered stdout line: '%s'", self._name, line)
        if self._deferred:
            self._outLines.append(line)
        
    def errFilteredLineReceived(self, line):
        self.logger.debug("[%s] Received filtered stderr line: '%s'", self._name, line)
        if self._deferred:
            self._errLines.append(line)
        
    def outLineReceived(self, line):
        if self._filterFunc(line):
            self.outFilteredLineReceived(line)

    def errLineReceived(self, line):
        if self._filterErr:
            if self._filterFunc(line):
                self.errFilteredLineReceived(line)
        else:
            self._errLines.append(line)
