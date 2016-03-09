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

# Guernsey example application - Template Demo

The template demo application demonstrates a slightly more complex use
of templates, with a fake database table and examples of how this can
be shown on a web page using a template, as well as how to format it
as JSON and CSV. This includes an example of the mechanism to enable
an additional media type producer for a resource.

To run it, make sure you are in your virtual environment. Also make
sure that you have the Cheetah template engine installed (should be
installed if you followed example 2). Then go to the application
directory and start the application:

  % ./bin/template-demo.py --log-level-console=DEBUG

Try visiting http://localhost:8080/ in your web browser. It should
show a simple web page with a title and today's date. The title and
the date are provided as key/value pairs to the template engine and
the rest is provided as a Cheetah template. This is just as in example
2.

But now the page also contains a link to a resource called
'cities'. This resource is implemented by the CitiesResource class,
and contains a small dictionary to emulate a table fetched from a
database. Depending on the media type requested, this table can be
formatted into HTML, JSON or CSV format. Try clicking the link in your
web browser. This should show a short table with a few cities and the
countries they are located in.

Now, if you take a look into the templates directory, you will notice that
the two template files have file names matching the class name of the
resource class. This is the default behavior, but it can be overridden
by calling the self.fillTemplate() method (which optionally takes a
templateFile parameter) from the getHtml() method, instead of just
returning the template model. If this is used, the processed template
string returned from self.fillTemplate() should be returned from the
getHtml() method, thus bypassing any later template processing. The
specified template file must exist on the template search path (which
can be specified as a command-line option), or a MissingTemplateError
exception will be raised.

We have now established that getHtml() can return either a model
object, which is processed in the templating system, or a string,
which will be passed directly to the client. There is a third option,
and that is to return the special constant
twisted.web.server.NOT_DONE_YET. This is used for deferred responses,
where the result cannot be immediately delivered to the client. This
may happen if the response needs to be produced by contacting an
external web service, a database server or by running an external
command.

Since these operations may block waiting for a response to be
delivered, they must be handled in a way that does not block the
reactor, since that would completely negate the advantages of using an
event-based programming framework like Twisted. More on this in a
later example.

Now, to get back on the main track, go to a terminal, and run
the following command:

  % curl -i -H "Accept: application/json,*/*;q=0.5" http://localhost:8080/cities/

This will produce a couple of HTTP headers as well as a JSON
object representing the cities table. Now run the following command:

  % curl -i -H "Accept: text/csv,*/*;q=0.5" http://localhost:8080/cities/

This should produce the cities table formatted as CSV.
