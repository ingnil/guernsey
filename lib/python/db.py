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
# Database classes
#

import copy
import os
import cPickle as pickle
import json
import base64

import guernsey.util as util

import __builtin__

class IdError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class Table(object):
    __deepcopy = True
    logger = None
    __database = None

    def __init__(self, tableName, database=None, deepCopy=True, persist=True):
        self.__tableName = tableName
        self.__deepCopy = deepCopy
        self.__database = database
        self.__persist = persist
        setattr(self, tableName, {})
        if not self.__class__.logger:
            self.__class__.logger = util.getLogger(self)

    def __getstate__(self):
        odict = self.__dict__.copy()
        if not self.__persist:
            odict[self.__tableName] = {}
        return odict

    def __setstate__(self, state):
        self.__dict__.update(state)
        if not self.__class__.logger:
            self.__class__.logger = util.getLogger(self)

    def getDatabase(self):
        return self.__database

    def setDatabase(self, database):
        self.__database = database

    def __getTable(self, getCopy=False):
        table = getattr(self, self.__tableName)
        if getCopy:
            if self.__deepcopy:
                return copy.deepcopy(table)
            else:
                return copy.copy(table)
        else:
            return table
    
    def get(self, id, default=None, getCopy=True):
        element = self.__getTable().get(id, default)
        if getCopy:
            if self.__deepcopy:
                return copy.deepcopy(element)
            else:
                return copy.copy(element)
        else:
            return element

    def getAll(self, getCopy=True):
        return self.__getTable(getCopy)
    
    def iteritems(self, getCopy=True):
        table = self.__getTable(getCopy)
        return table.iteritems()

    def iterkeys(self, getCopy=True):
        table = self.__getTable(getCopy)
        return table.iterkeys()

    def itervalues(self, getCopy=True):
        table = self.__getTable(getCopy)
        return table.itervalues()

    def set(self, id, model):
        if id is __builtin__.id:
            raise IdError("Tried to set model with builtin function id as key")
        self.__getTable()[id] = model

    def update(self, id, model, createIfNotFound=False):
        if id is __builtin__.id:
            raise IdError("Tried to update model with builtin function id as key")
        element = self.__getTable().get(id)
        if element:
            element.update(model)
        elif createIfNotFound:
            self.__getTable()[id] = model
        else:
            raise KeyError("Table '%s' has no key '%s'" % (self.__tableName, id))

    def delete(self, id):
        if id is __builtin__.id:
            raise IdError("Tried to delete model with builtin function id as key")
        if self.__getTable().get(id):
            del self.__getTable()[id]
        else:
            raise KeyError("Table '%s' has no key '%s'" % (self.__tableName, id))

    def clear(self):
        table = self.__getTable()
        table.clear()

    def __repr__(self):
        output = self.__class__.__name__ + "{"

        members = []
        for k, v in self.__dict__.iteritems():
            if k in ["_Table__database", "logger"]:
                continue
            members.append("%s: %r" % (k, v))

        output += ", ".join(members) + "}"
        return output

class Database(object):
    logger = None
    preferJson = False

    def __init__(self):
        if not self.__class__.logger:
            self.__class__.logger = util.getLogger(self)

    def __setstate__(self, state):
        if not self.__class__.logger:
            self.__class__.logger = util.getLogger(self)
        self.logger.debug("__setstate__(...)")
        self.__dict__.update(state)

    @staticmethod
    def _computeJsonFilename(filename):
        path, name = os.path.split(filename)
        base, ext = os.path.splitext(name)
        jsonName = ".".join([base, "json"])
        return os.path.join(path, jsonName)

    @classmethod
    def _loadJson(cls, filename):
        jsonFh = open(filename, "r")
        jsonDb = json.load(jsonFh)
        jsonFh.close()
        db = cls()
        backRefTables = []
        for tableName, b64PickledTable in jsonDb.iteritems():
            pickledTable = base64.b64decode(b64PickledTable)
            table = pickle.loads(pickledTable)
            if tableName == "_backRefTables":
                backRefTables = table
                continue
            setattr(db, tableName, table)

        for tableName in backRefTables:
            getattr(db, tableName).setDatabase(db)

        for tableName, table in db.__dict__.iteritems():
            table = cls._loadJsonTableTransform(db, tableName, table)
            setattr(db, tableName, table)

        return db

    @classmethod
    def _loadJsonTableTransform(cls, database, tableName, table):
        return table

    @classmethod
    def _loadPickle(cls, filename):
        f = open(filename, "r")
        o = pickle.load(f)
        f.close()
        if hasattr(o, "_loadPickleTransform"):
            o._loadPickleTransform()
        return o

    def _loadPickleTransform(self):
        pass

    @classmethod
    def load(cls, filename):
        if not cls.logger:
            cls.logger = util.getLogger(cls)
        jsonPath = cls._computeJsonFilename(filename)
        if cls.preferJson and os.path.exists(jsonPath):
            return cls._loadJson(jsonPath)
        else:
            return cls._loadPickle(filename)

    def _saveJson(self, filename):
        self.logger.debug("_saveJson(%r)", filename)
        jsonPath = self._computeJsonFilename(filename)
        tmpJsonPath = "%s.new" % jsonPath

        tables = {}
        for tableName, table in self.__dict__.iteritems():
            if isinstance(table, Table):
                tables[tableName] = copy.copy(table)

        backRefTables = []
        for tableName, table in tables.iteritems():
            if table.getDatabase():
                self.logger.debug("Table %s has database backreference", tableName)
                self.logger.debug("Removing backreference and storing table name")
                backRefTables.append(tableName)
                table.setDatabase(None)
        tables["_backRefTables"] = backRefTables

        db = {}
        for tableName, table in tables.iteritems():
            table = self._saveJsonTableTransform(tableName, table)
            pickledTable = pickle.dumps(table)
            b64PickledTable = base64.b64encode(pickledTable)
            db[tableName] = b64PickledTable

        try:
            f = open(tmpJsonPath, "w")
            json.dump(db, f)
            f.close()
            os.rename(tmpJsonPath, jsonPath)
        except:
            self.logger.exception("Could not save JSON database")
            os.unlink(tmpJsonPath)

    @classmethod
    def _saveJsonTableTransform(cls, tableName, table):
        return table

    def _savePickle(self, filename):
        self.logger.debug("_savePickle(%r)", filename)
        self._savePickleTransform()
        tmpFilename = "%s.new" % filename
        try:
            f = open(tmpFilename, "w")
            pickle.dump(self, f)
            f.close()
            os.rename(tmpFilename, filename)
        except:
            self.logger.exception("Could not save database")
            os.unlink(tmpFilename)

    def _savePickleTransform(self):
        self.logger.debug("_savePickleTransform()")

    def save(self, filename):
        self.logger.debug("save(%r)", filename)
        self._savePickle(filename)
        self._saveJson(filename)
        
    def __repr__(self):
        output = self.__class__.__name__ + "{"

        members = []
        for k, v in self.__dict__.iteritems():
            members.append("%s: %r" % (k, v))

        output += ", ".join(members) + "}"
        return output
