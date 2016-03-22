#!/usr/bin/env python
#
#    Guernsey - Library to simplify creating REST web services using Python and Twisted
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

import guernsey.web.rest as rest
import guernsey.web.model as gwm
import guernsey.protocol.process as gpp
import guernsey.web.json as json
import guernsey.util as util

from twisted.internet import defer, reactor
from twisted.web import server

import os

#
# Create a model class for processes, inheriting from the Guernsey
# Model class. We do not include every field in this class. This is
# left as an exercise to the reader.
#

class ProcessModel(gwm.Model):
    user = None
    pid = None
    cpu = None
    mem = None
    command = None

#
# Create a resource class for processes. It will produce HTML and
# JSON, but we skip CSV this time, since that is already covered in
# example 3.
#

class ProcessesResource(rest.Resource):
    requireAuth = True

    #
    # This method was created to allow a child class to use another
    # protocol class (in this case
    # guernsey.protocol.process.FilteredLineReceiverProtocol, while
    # reusing the rest of the code.
    #
    def createProcessProtocol(self, name, deferred):
        return gpp.LineReceiverProtocol(name, deferred)
        
    #
    # This method is called to get a list of processes using the "ps
    # au" command. But since running an external command may take some
    # time, we do not want to just use the standard Python library
    # functions, since those would block the reactor and prevent the
    # application from serving other clients while the external
    # command is running.
    #
    # To solve this, Twisted supplies something called a process
    # protocol class. This allows the application to react to process
    # events, such as command output and command termination, while
    # the process is running without blocking the reactor. Since the
    # Twisted process protocol class just defines the interface,
    # Guernsey supplies a couple of more useful protocol classes in
    # the guernsey.protocol.process package.
    #
    # The method starts by creating a Deferred instance, which is a
    # placeholder for a future result. To get hold of the actual
    # result later, we add callbacks to this deferred instance that
    # will process the result when it becomes available. For example,
    # when the external process is done, our process protocol class
    # will pass captured output and error streams as well as the exit
    # code to the first callback in the callback chain.
    #
    # If an error occurs, it will instead call the first error
    # callback, or "errback" in the errback chain. If the errback can
    # solve the problem, it can then pass its result to the next
    # callback in the callback chain. Thus, a result can be processed
    # by parts of both the callback and errback chains. The
    # interactions of various codepaths through these chains is a
    # fairly complicated topic, and will not be investigated deeply
    # here.
    #
    # Wait, what callback (and errback) chain? Well, it is possible to
    # add several callbacks and errbacks to a Deferred instance. When
    # the result becomes available, it is passed to the first callback
    # in the chain. The return value from the first callback is passed
    # as the argument to the second callback in the callback chain,
    # and so on. Add the errback chain too and the topic becomes
    # fairly complex.
    #
    # Getting back on track, this method creates a deferred, passes it
    # to the process protocol, adds a callback and errback, spawns the
    # external process, and returns it to the caller. Since the cb()
    # inner method defined here is the first callback in the callback
    # chain (since the deferred is also created in the below method),
    # this cb() method will get the result from the process protocol
    # when the external process is done. It then returns the captured
    # standard output lines to the next callback in the callback chain
    # (if such a callback exists). For more information on callback
    # and errback chains, please consult the Twisted manual. For more
    # information about inner methods, please consult the Python
    # manual.
    #
    def getProcessList(self):
        deferred = defer.Deferred()
        pp = self.createProcessProtocol("ps au", deferred)

        def cb(result):
            self.logger.debug("getProcessList() cb(%r)", result)
            return result["stdout"]

        def eb(failure):
            self.logger.debug("getProcessList() eb(%r)", failure)
            if isinstance(failure.type, Exception):
                util.logTwistedFailure(self.logger, failure,
                                       "Exception thrown while getting process list")
            return []

        deferred.addCallbacks(cb, eb)
        
        args = ["ps", "au"]
        reactor.spawnProcess(pp, args[0], args, env=os.environ, path=None, usePTY=False)
        return deferred

    #
    # This method is called to get a list of processes and then
    # process the result. It does this by calling
    # self.getProcessList(), which returns a deferred with one
    # callback and one errback already in its callback and errback
    # chains. It then adds its own callback and errback to the
    # callback and errback chains of the deferred, and returns the
    # deferred to the caller.
    #
    # If all goes well, the result from the self.getProcessList() cb()
    # method is supplied as the argument to our cb() method below. The
    # main part of the processing is performed in that callback. The
    # callback takes a set of output lines from the "ps au" command,
    # strips the header and converts each remaining line into a
    # ProcessModel instance. This is added to a list, and when all
    # lines have been processed, the list of ProcessModel instances is
    # returned from the callback. This causes it to be passed as an
    # argument to the next callback in the callback chain.
    #
    # This method is used by both getHtml() and getJson() to produce a
    # common data model for this resource, which the format producer
    # methods then tailor to their specific needs.
    #
    def prepareProcessList(self):
        deferred = self.getProcessList()
        
        processModels = []

        def cb(processLines):
            self.logger.debug("prepareProcessList() cb(%r)", processLines)
            for processLine in processLines[1:]:
                fields = processLine.split(None, 10)
                pm = ProcessModel()
                pm.user = fields[0]
                pm.pid = fields[1]
                pm.cpu = fields[2]
                pm.mem = fields[3]
                pm.command = fields[-1]
                processModels.append(pm)
            return processModels

        def eb(failure):
            self.logger.debug("prepareProcessList() eb(%r)", failure)
            if isinstance(failure.type, Exception):
                util.logTwistedFailure(self.logger, failure,
                                       "Exception thrown while getting process list")
            return processModels

        deferred.addCallbacks(cb, eb)
        return deferred

    #
    # This method gets a list of process models, adapts it for
    # processing by a HTML template, and returns the result.
    #
    # Just like in the methods above, the reality is a bit more
    # complicated. It gets a deferred object from
    # self.prepareProcessList(), and adds its own callback and errback
    # methods to the callback and errback chains. It then returns a
    # special constant, twisted.web.server.NOT_DONE_YET. This is
    # crucial, since it tells the framework that the result is not
    # complete, and that a return value will be produced by a callback
    # later.
    #
    # Another crucial part takes place in both the callback and
    # errback methods. Both these methods prepare a response, and
    # after using request.write() to send the response to the client,
    # they call request.finish(). This call is very important, since
    # if this method is not called, the framework has no way of
    # knowing that the result has been sent in its entirety, and will
    # hang forever waiting for additional data to be sent to the
    # client.
    #
    # As you can see, the HTML code needs to be generated by a manual
    # call to self.fillTemplate(). This is in essence what the
    # framework does when a dictionary is returned from the getHtml()
    # method, except the framework does not process the model in any
    # way.
    #
    def getHtml(self, request):
        self.logger.debug("getHtml(%r)", request)
        if self.checkPermission(request):
            self.logger.debug("User has permission to access this resource")
        else:
            self.logger.debug("User does NOT have permission to access this resource")
            self.forbidden(request)
            return "Forbidden"

        deferred = self.prepareProcessList()

        def cb(processes):
            self.logger.debug("getHtml() cb(%r)", processes)
            request.write(self.fillTemplate(model = {
                        "processes": sorted(processes, key=lambda x: int(x.pid))
                        }))
            request.finish()
            
        def eb(failure):
            self.logger.debug("getHtml() eb(%r)", failure)
            if isinstance(failure.type, Exception):
                util.logTwistedFailure(self.logger, failure,
                                       "Exception thrown while getting process list")
            self.serverError(request)
            request.write("Internal Server Error")
            request.finish()
        
        deferred.addCallbacks(cb, eb)
        return server.NOT_DONE_YET

    #
    # This method works the same way as the getHtml() method above,
    # but as expected, the callback produces JSON instead of HTML, and
    # does not call the template engine.
    #
    # Note that we use our own JSON encoder. This is actually just an
    # extension to the JSON encoder provided by the standard library,
    # but it has a few nice features that the standard JSON encoder
    # doesn't have. For example, it allows each class to define its
    # own JSON encoder method, called __json__(), which will be called
    # if available to convert an object to JSON.
    #
    def getJson(self, request):
        deferred = self.prepareProcessList()

        def cb(processes):
            self.logger.debug("getJson() cb(%r)", processes)
            request.write(json.dumps({"processes": processes}))
            request.finish()
            
        def eb(failure):
            self.logger.debug("getJson() eb(%r)", failure)
            if isinstance(failure.type, Exception):
                util.logTwistedFailure(self.logger, failure,
                                       "Exception thrown while getting process list")
            self.serverError(request)
            request.write(json.dumps({"error": "500 Internal Server Error"}))
            request.finish()
        
        deferred.addCallbacks(cb, eb)
        return server.NOT_DONE_YET

#
# Create a resource class for processes owned by the user root. It
# will produce HTML and JSON. This class inherits everything from the
# ProcessesResource created above, but substitutes the
# LineReceiverProtocol for a FilteredLineReceiverProtocol
# instead. This resource just illustrates the use of that class.
#
# Note that we also reuse the template file from the parent class. If
# we did not specify it here, the framework would try to use our class
# name to construct a template filename, and no such template exists.
#
class RootProcessesResource(ProcessesResource):
    def __init__(self, parent):
        ProcessesResource.__init__(self, parent)
        self.setTemplateName("ProcessesResource.tmpl")

    def createProcessProtocol(self, name, deferred):
        return gpp.FilteredLineReceiverProtocol(name,
                                                lambda x: x.startswith("root"),
                                                deferred=deferred)

#
# Create your application class, inheriting from the Guernsey RootResource class
#

class AuthTest(rest.RootResource):
    #
    # Set a few usage parameters, used by the online help system
    #
    version = "0.1"
    desc = "Authentication & Authorization test application"
    usage = "Usage: %prog [OPTIONS]"

    #
    # Define a constructor for your application class, calling the
    # RootResource constructor in turn. Then add instances of the
    # ProcessesResource class and the RootProcessesResource as child
    # resources.
    #
    def __init__(self):
        rest.RootResource.__init__(self, appName="AuthTest",
                                   appId="guernsey-auth-test")
        self.putChild("processes", ProcessesResource(self))
        self.putChild("root-processes", RootProcessesResource(self))


#
# Main method
#

def main():
    app = AuthTest()
    app.run()
    
if __name__ == '__main__':
    main()
