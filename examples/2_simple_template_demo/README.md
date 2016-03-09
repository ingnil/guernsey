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

# Guernsey example application - Simple Template Demo

The simple template demo application introduces the use of templates.

To run it, make sure you are in your virtual environment. Also make
sure that you have the Cheetah template engine installed. Then go to
the application directory and start the application:

  % ./bin/simple-template-demo.py --log-level-console=DEBUG

Try visiting http://localhost:8080/ in your web browser. It should
show a simple web page with a title and today's date. The title and
the date are provided as key/value pairs to the template engine and
the rest is provided as a Cheetah template.

Go to another terminal, and run the following command:

  % curl -i -H "Accept: application/json,*/*;q=0.5" http://localhost:8080/

It will hopefully produce a couple of HTTP headers as well as a JSON
object. You will probably notice that the JSON object is still a hello
world message. This is because our application class does not provide
a getJson() method, so the default is used.

Try adding the following code to the SimpleTemplateDemo class:

        def getJson(self, request):
    	    return self.getData()

Restart the application and run the curl command above again. This
should return a JSON object containing the same key/value pairs that
we provided to the Cheetah template engine in the getHtml() method.
