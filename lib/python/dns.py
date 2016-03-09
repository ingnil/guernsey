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
# DNS resolver classes
#

from twisted.names import client

import guernsey.util as util

class DnsClient(object):
    logger = None

    def lookupService(self, name, timeouts=[2]):
        self.logger.debug("lookupService(name=%r, timeouts=%r)", name, timeouts)
        deferred = client.lookupService(name, timeouts)

        def cb(result):
            self.logger.debug("lookupService() cb(result=%r)", result)
            payload = result[0][0].payload
            port = payload.port
            name = payload.target.name
            return (name, port)

        def eb(failure):
            self.logger.warning("lookupService(name=%r, timeouts=%r) eb(failure=%r)",
                                name, timeouts, failure)
            if isinstance(failure.type, Exception):
                util.logTwistedFailure(self.logger, failure,
                                       "lookupService(name=%r, timeouts=%r) threw exception",
                                       name, timeouts)
            self.logger.warning("failure.__dict__: %r", failure.__dict__)
            return (None, None)

        deferred.addCallbacks(cb, eb)
        return deferred

DnsClient.logger = util.getLogger(DnsClient)
