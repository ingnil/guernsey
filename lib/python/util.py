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
# Handy utility functions
#

def convertToCamelCase(string, sep="-"):
    parts = string.split(sep)
    if len(parts) > 1:
        for i, part in enumerate(parts[1:], start=1):
            parts[i] = part.capitalize()
    return "".join(parts)

def convertFromCamelCase(string, sep="-"):
    dest = ""

    for c in string:
        if c.isupper():
            dest += sep + c.lower()
        else:
            dest += c
    return dest

def getLogger(o):
    import logging, inspect

    if inspect.isclass(o):
        cls = o
    else:
        cls = o.__class__

    module = cls.__module__
    if module == '__main__':
        fqcn = cls.__name__
    else:
        fqcn = ".".join([cls.__module__, cls.__name__])
    return logging.getLogger(fqcn)

def logTwistedFailure(logger, failure, msg, *args):
    return logger.exception(msg, *args, exc_info=(failure.type, failure.value, failure.frames))
