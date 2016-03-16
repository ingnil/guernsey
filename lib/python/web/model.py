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
# Common base class for data models
#

import guernsey.util as util
from guernsey import Object

class Model(Object):
    def __init__(self, record=None):
        Object.__init__(self)
        if type(record) == dict:
            for k, v in record.iteritems():
                setattr(self, k, v)

    def update(self, newModel):
        for key, value in newModel.__dict__.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        output = self.__class__.__name__ + "{"

        members = []
        for k, v in self.__dict__.iteritems():
            members.append("%s: %r" % (k, v))

        output += ", ".join(members) + "}"
        return output

    def __json__(self):
        return self.__dict__
