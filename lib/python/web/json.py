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
# Improved JSON encoder
#

from __future__ import absolute_import

import json
import datetime

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__json__"):
            return obj.__json__()
        if type(obj) == datetime.datetime:
            return {"secondsSinceEpoch": (obj - datetime.datetime(1970, 1, 1)).total_seconds(),
                    "iso8601Full": obj.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "iso8601": obj.strftime("%Y-%m-%d %H:%M:%S")}
        if type(obj) == set or type(obj) == frozenset:
            return list(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def dump(obj, fp):
    return json.dump(obj, fp, cls=JsonEncoder)

def dumps(obj):
    return json.dumps(obj, cls=JsonEncoder)

def load(fp):
    return json.load(fp)

def loads(s):
    return json.loads(s)
