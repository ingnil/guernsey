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
# This module provides classes for serving clients on a local socket
# (Unix domain socket)
#

from twisted.internet import protocol
from twisted.protocols import basic

import guernsey.util as util

import os

class LocalSocketProtocol(basic.LineOnlyReceiver):
    logger = None
    delimiter = '\n'
    factory = None
    commandMap = None

    def __init__(self, factory, commandMap={}):
        if not self.__class__.logger:
            self.__class__.logger = util.getLogger(self)
        self.logger.debug("__init__(%r)", factory)
        self.factory = factory
        self.commandMap = commandMap

    def lineReceived(self, line):
        if line in self.commandMap:
            self.logger.debug("Command '%s' received", line)
            self.commandMap[line]()
        else:
            self.logger.warning("Received unrecognized line: %s", line)

class LocalSocketProtocolFactory(protocol.Factory):
    logger = None
    app = None
    protocolClass = LocalSocketProtocol

    def __init__(self, app):
        if not self.__class__.logger:
            self.__class__.logger = util.getLogger(self)
        self.logger.debug("__init__(%r)", app)
        self.app = app

    def buildProtocol(self, addr):
        self.logger.debug("buildProtocol(%r)", addr)
        return self.protocolClass(self)
