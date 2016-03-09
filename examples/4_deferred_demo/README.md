<!--
    Guernsey - Library to simplify creating REST web services using Python and Twisted
    Copyright (C) 2016 Ingemar Nilsson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->

# Guernsey example application - Deferred Demo

The deferred demo application demonstrates the common case that the
data needed to produce a result for a request is not immediately
available. An external command might need to be executed, a database
might need to be queried, or an external web service might need to be
called.

If performed in the common way, such an operation would probably
block, i.e. leave the application stalled while waiting for a
reply. In an application built on an event-driven framework like
Twisted, this would block the single-threaded main loop and prevent
the application from serving other clients while waiting. This would
in turn render the advantage of using such a framework null and void.

Thus we need to perform this operation in a way that does not block
the reactor. In this case, we have two resources that run an external
command to produce the result they need. This is done through the use
of a process protocol, which is attached to a spawned process and used
to handle events concerning that process. The reactor continues to run
and is able to serve other clients while we wait for the external
process to complete. When the process is done, the process protocol
passes the result to a callback chain set up by our resource class. If
everything works out as intended, the result is processed through
several callbacks to produce a web page or a JSON object in the
end. The code contains fairly detailed comments on how this works.

To run it, make sure you are in your virtual environment. Then go to
the application directory and start the application:

  % ./bin/deferred-demo.py --log-level-console=DEBUG

Try visiting http://localhost:8080/ in your web browser. It should
show a simple web page with links to two subpages (handled by our two
resource classes mentioned above), /processes/ and /root-processes/.

Try clicking the link named "All Processes" in your web browser. This
should show a table of all processes running on your computer, with
several fields describing each process. This page is produced by first
creating a deferred object, then creating a process protocol using
that deferred. This process protocol is then passed to the
reactor.spawnProcess() method along with the command name and
arguments. The external command is spawned and the process protocol is
attached to it. The format producer (getHtml() or getJson() in this
case) then returns twisted.web.server.NOT_DONE_YET to the framework,
so that the reactor can serve other clients wile we are waiting.

The process protocol takes care of asynchronously handling events
related to our spawned process. In this case, the process protocol
collects the output streams from the external process, splits it into
lines, and when the process is done, it calls the callback chain on
the deferred object that we set up earlier with the output lines that
it has captured.

The callback chain receives the lines, removes the first (which
contains the header), splits each remaining line into fields, and
constructs a ProcessModel instance from the fields. All process models
are collected in a list, and this list is processed into either HTML
or JSON depending on the media type requested. Finally, the response
is sent to the client, and the last callback tells the framework that
the response is complete.

Now, to get back on the main track, go to a terminal, and run
the following command:

  % curl -i -H "Accept: application/json,*/*;q=0.5" http://localhost:8080/processes/

This will produce a couple of HTTP headers as well as a JSON
object representing the processes table. Now run the following command:

  % curl -i -H "Accept: text/csv,*/*;q=0.5" http://localhost:8080/processes/

Did you expect that? We actually received the result as HTML. This is
because we did not care to create a format producer for text/csv, but
we also specified */* as an acceptable media type in the curl command
above. Thus, it works as intended. We specified that we want text/csv,
but that any format is acceptable if text/csv is not available. Try
removing the */* media type from the line above, like this:

  % curl -i -H "Accept: text/csv" http://localhost:8080/processes/

This should produce a 406 Not Acceptable error. This means that the
server is unable to produce a response in the requested format.

Try rerunning the following command:

  % curl -i -H "Accept: text/csv,*/*;q=0.5" http://localhost:8080/processes/

There is currently a bug in the library that is visible in the output
from the request above. Can you spot what it is? I'll spoil it for
you. The Content-Type header contains the value */*, while it should
contain the value text/html. This is because the code currently does
not differentiate between the requested content type and the actual
produced content type. This will be fixed in a future release.

If you want, you can go back to the root page in your web browser and
click on the "Processes owned by root" instead. This should show a
table of processes owned by root running on your system. You can also
try visiting that resource using curl with various requested media
types. Creating the curl commands to do that is left as an exercise to
the reader.
