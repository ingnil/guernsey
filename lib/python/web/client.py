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
# This module provides WebClient, a wrapper class around the Twisted
# Web Client.
#

from twisted.web.client import Agent
from twisted.internet import reactor, protocol, defer
from twisted.web.http_headers import Headers
from twisted.web.client import FileBodyProducer

import guernsey.web.json as json
import guernsey.util as util

import urllib
from StringIO import StringIO
import logging

class WebClient(object):
    userAgent = "WebClient"
    contentType = "application/x-www-form-urlencoded"
    accept = "application/json"
    logger = None

    def __init__(self):
        self.extraHeaders = {}

    def setUserAgent(self, ua):
        self.userAgent = ua

    def setContentType(self, ct):
        self.contentType = ct

    def setAccept(self, a):
        self.accept = a

    def setHeader(self, key, value):
        self.extraHeaders[str(key)] = [ str(value) ]

    def sendRequest(self, url, method, data=None):
        self.logger.debug("sendRequest(%r, %r, %r)", url, method, data)

        if type(data) == dict:
            if self.contentType == "application/json":
                data = json.dumps(data)
            else:
                data = urllib.urlencode(data)
            self.logger.debug("Data after conversion: %r", data)

        headers = {'User-Agent': [ self.userAgent ],
                   'Accept': [ self.accept ]}
        if data:
            headers.update({'Content-Type': [ self.contentType ]})

        if self.extraHeaders:
            headers.update(self.extraHeaders)

        self.logger.debug("Request Headers:")
        if self.logger.isEnabledFor(logging.DEBUG):
            for k, v in headers.iteritems():
                self.logger.debug("\t%r: %r", k, v)
        
        agent = Agent(reactor)
        deferred = agent.request(
            method.upper(),
            url,
            Headers(headers),
            FileBodyProducer(StringIO(data)))

        def cb(response):
            self.logger.debug("sendRequest() cb(%r)", response)
            self.logger.info("Request %s %s (Data: %s):", method.upper(), url, data)
            self.logger.info("Response Code: %s", response.code)
            self.logger.debug("Response Phrase: %s", response.phrase)
            self.logger.debug("Response Length: %s", response.length)
            self.logger.debug("Response Headers:")
            if self.logger.isEnabledFor(logging.DEBUG):
                for k, v in response.headers.getAllRawHeaders():
                    self.logger.debug("\t%s: %r", k, v)
            return response

        deferred.addCallback(cb)
        return deferred

    def request(self, url, method, data=None, getBody=True):
        self.logger.debug("request(%r, %r, %r, %r)", url, method, data, getBody)

        responseDeferred = self.sendRequest(url, method, data)
        if not getBody:
            self.logger.debug("Will not get response body")
            return responseDeferred

        def cb(response):
            self.logger.debug("request() cb(%r)", response)
            if not 200 <= response.code < 300:
                self.logger.debug("Request was not successful, will not get response body")
                return response

            self.logger.debug("Request was successful, will get response body")
            finished = defer.Deferred()

            def bodyCb(body):
                self.logger.debug("request() cb() bodyCb(%r)", body)
                response.body = body
                return response

            def bodyEb(failure):
                self.logger.debug("request() cb() bodyEb(%r)", failure)
                if isinstance(failure.type, Exception):
                    util.logTwistedFailure(self.logger, failure,
                                           "Exception thrown while getting body for "
                                           "request %s %s", method.upper(), url)

            finished.addCallbacks(bodyCb, bodyEb)
            response.deliverBody(BodyReceiver(finished))
            return finished

        def eb(failure):
            self.logger.debug("request() eb(%r)", failure)
            if isinstance(failure.type, Exception):
                util.logTwistedFailure(self.logger, failure,
                                       "Exception thrown while processing request %s %s",
                                       method.upper(), url)
            return failure

        responseDeferred.addCallbacks(cb, eb)
        return responseDeferred

    def get(self, url, data=None, getBody=True):
        self.logger.info("get(%r, %r, %r)", url, data, getBody)
        if data:
            if type(data) == dict:
                data = urllib.urlencode(data)
            url = "?".join([url, data])
        return self.request(url, "GET", data=None, getBody=getBody)

    def post(self, url, data, getBody=False):
        self.logger.info("post(%r, %r, %r)", url, data, getBody)
        return self.request(url, "POST", data, getBody=getBody)

    def put(self, url, data, getBody=False):
        self.logger.info("put(%r, %r, %r)", url, data, getBody)
        return self.request(url, "PUT", data, getBody=getBody)

    def delete(self, url, getBody=False):
        self.logger.info("delete(%r, %r)", url, getBody)
        return self.request(url, "DELETE", data=None, getBody=getBody)

WebClient.logger = util.getLogger(WebClient)

class BodyReceiver(protocol.Protocol):
    logger = None

    def __init__(self, finished):
        self.finished = finished
        self.body = ""

    def dataReceived(self, bytes):
        self.logger.debug("dataReceived(%r)", bytes)
        self.body += bytes

    def connectionLost(self, reason):
        self.logger.debug("connectionLost(%r)", reason)
        self.finished.callback(self.body)

BodyReceiver.logger = util.getLogger(BodyReceiver)
