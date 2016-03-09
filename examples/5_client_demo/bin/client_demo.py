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
import guernsey.web.client as webclient

from twisted.internet import defer
from twisted.web import server

#
# We reuse the model class from example 4.
#

class ProcessModel(gwm.Model):
    user = None
    pid = None
    cpu = None
    mem = None
    command = None

#
# Create a resource class for processes. Unlike in example 4, this
# class will not spawn an external process to fetch the data. Instead,
# it will fetch the information from a running instance of example 4
# using HTTP.
#
class ProcessesResource(rest.Resource):
    #
    # We moved the RootProcessesResource so that it is now a child of
    # this resource. This enables it to call the methods in this
    # resource class without inheriting from it.
    #
    def __init__(self, parent):
        rest.Resource.__init__(self, parent)
        self.putChild("root", RootProcessesResource(self))

    #
    # This method gets a list of processes from a running instance of
    # example 4. We take the URL to that application from the options
    # attribute on the root resource, i.e. the ClientDemo class. This
    # attribute contains options specified on the command line. How we
    # added this command-line option is explained in the comments for
    # the ClientDemo class below.
    #
    # The web client get() method returns a deferred object when
    # called, since fetching data from an external web service might
    # take some time, and we do not want to block the reactor while we
    # are waiting. This should be a bit more familiar this time, if
    # you worked through example 4.
    #
    # The default media type requested by the web client is
    # application/json, so we do not have to specify that
    # manually. This time, the callback receives a response object,
    # containing the reponse headers as well as the response
    # body. Because we requested JSON, the response body is simply a
    # JSON object.
    #
    # Thus, the callback simply decodes the JSON object and converts
    # the list into a list of ProcessModel instances. This process is
    # simplified through the reuse of the same ProcessModel class,
    # which allows us to import the data directly into our process
    # model from the decoded JSON object. The list of process models
    # is then returned from the callback, i.e. passed to the next
    # callback in the callback chain.
    #
    def getProcessList(self):
        client = webclient.WebClient()
        url = self.getRoot().options.processesUrl
        
        deferred = client.get(url)

        def cb(response):
            self.logger.debug("getProcessList() cb(%r)", response)

            responseObj = json.loads(response.body)
            processList = responseObj["processes"]
            processModels = []
            for process in processList:
                model = ProcessModel(process)
                processModels.append(model)
            return processModels

        def eb(failure):
            self.logger.debug("getProcessList() eb(%r)", failure)
            if isinstance(failure.type, Exception):
                util.logTwistedFailure(self.logger, failure,
                                       "Exception thrown while getting process list")
            return []

        deferred.addCallbacks(cb, eb)
        return deferred

    #
    # The getHtml() method is copied almost verbatim from example
    # 4. The only difference is the call to getProcessList(), since
    # this class does not contain any prepareProcessList() method.
    #
    def getHtml(self, request):
        deferred = self.getProcessList()

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
    # The getJson() method is copied almost verbatim from example
    # 4. The only difference is the call to getProcessList(), since
    # this class does not contain any prepareProcessList() method.
    #
    def getJson(self, request):
        deferred = self.getProcessList()

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
# Create a resource class for processes owned by the user root. Since
# this class is now a child of ProcessesResource, we can call the
# getProcessList() method of that class by using getParent().
#
# The data returned is processed in the callback by filtering the
# process list on the ProcessModel 'user' attribute, so that the
# filtered list only contains processes owned by root. The filtered
# list is then passed to the template system just like in example 4.
#
class RootProcessesResource(rest.Resource):
    def __init__(self, parent):
        rest.Resource.__init__(self, parent)
        self.setTemplateName("ProcessesResource.tmpl")

    def getHtml(self, request):
        deferred = self.getParent().getProcessList()

        def cb(processes):
            self.logger.debug("getHtml() cb(%r)", processes)
            filteredProcesses = filter(lambda x: x.user == "root", processes)
            request.write(self.fillTemplate(model = {
                        "processes": sorted(filteredProcesses, key=lambda x: int(x.pid))
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

    def getJson(self, request):
        deferred = self.getParent().getProcessList()

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
# Create your application class, inheriting from the Guernsey RootResource class
#

class ClientDemo(rest.RootResource):
    #
    # Set a few usage parameters, used by the online help system
    #
    version = "0.1"
    desc = "WebClient example application"
    usage = "Usage: %prog [OPTIONS]"

    #
    # Define a constructor for your application class, calling the
    # RootResource constructor in turn. Then add an instance of the
    # ProcessesResource class as a child resource.
    #
    def __init__(self):
        rest.RootResource.__init__(self, appName="ClientDemo",
                                   appId="guernsey-client-demo")
        self.putChild("processes", ProcessesResource(self))

    #
    # We override this method of the RootResource class to add our own
    # command-line interface (CLI) argument. The 'parser' argument is
    # a standard optparse parser object.
    #
    def optparsePostInit(self, parser):
        parser.add_option("--processes-url", action="store", type="str",
                          dest="processesUrl", metavar="URL",
                          help="URL to get process list from (Default: %default)")
        parser.set_defaults(processesUrl="http://localhost:8090/processes/")

    #
    # We override this method of the RootResource class to add
    # validation of our added CLI arguments. 
    #
    def optparsePostParse(self, parser, options, args):
        if not options.processesUrl.startswith("http"):
            parser.error("Processes URL must start with 'http'")

#
# Main method
#

def main():
    app = ClientDemo()
    app.run()
    
if __name__ == '__main__':
    main()
