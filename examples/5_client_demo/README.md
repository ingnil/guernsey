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

# Guernsey example application - Client Demo

The client demo application demonstrates the use of the Guernsey web
client. We will use example 4 as a data source for this aplication.

First, open a new terminal and activate the virtual environment. Then
go to the example 4 directory and start it, but on the port 8090
instead:

  % ./bin/deferred-demo.py --log-level-console=DEBUG

Go back to your main terminal and make sure you are in your virtual
environment. Then go to the application directory and start the
application:

  % ./bin/client-demo.py --log-level-console=DEBUG

Try visiting http://localhost:8080/ in your web browser. It should
show a simple web page with a link to one subpage, /processes/.

Try clicking the link named "All Processes" in your web browser. This
should show a table of all processes running on your computer, with
several fields describing each process. This page is produced by the
server through contacting the example 4 application and requesting the
/processes/ resource as JSON. Thus the server is acting as a client
when communicating with the example 4 app. The example 5 server then
gets and decodes a JSON object containing a list of all processes,
converts it to a list of process models, and hands this list to the
templating system, producing an HTML page.

More specifically, the web client subsystem sends a request to the
example 4 web server, and returns a deferred object. We then attach
callbacks to it to decode the returned JSON object and finally produce
a web page when the reply from the example 4 web server has arrived.

Now, go to a terminal and run the following command:

  % curl -i -H "Accept: application/json,*/*;q=0.5" http://localhost:8080/processes/

This will produce a couple of HTTP headers as well as a JSON
object representing the processes table.

One can note that the JSON object returned in essence is equal to the
one returned from the example 4 application, even though it has been
decoded from JSON and then reencoded to JSON by the client demo
application. This is strictly speaking unnecessary, as we could have
simply forwarded the JSON object returned from our example 4 server
directly to the client.

In practice however, it is seldom the case that a third-party JSON
object has exactly the same format as JSON objects produced by your
own application. In addition, you might still want to perform
validation and security checks before sending the data to the client,
so this decode/encode step is useful in most cases even if it may seem
superfluous at a glance.

Now visit the URL http://localhost:8080/processes/root/ in your web
browser. This page calls the code in the ProcessesResource instance to
get the actual data, and then just removes the data items it does not
want. It also reuses the same template as ProcessesResource, which is
why there is a link to itself at the top of the page.

Go back to the /processes/ page. Now we will see what happens if we
close down the data source. Go to your terminal running the example 4
application and press CTRL-C. The application should shut down. Reload
the page.

What happens? It shows an empty table. This is because our error
handling is quite simple, and we just return an empty list from the
errback inner method of getProcessList(). We could have thrown an
exception instead, which would trigger the errback inner method of
getHtml(), which returns an error page instead. This is left as an
exercise for the reader.

Now try restarting the example 4 server, and everything should be
working when you reload the page again.
