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

# Guernsey example application - Hello World

The hello world application is pretty much as simple as it gets. The
code has ample comments, so it should be easy to follow.

To run it, make sure you are in your virtual environment, go to the
application directory and start the application:

```
./bin/helloworld.py
```

The application prints a few lines to the console and waits for
connections. Try visiting `http://localhost:8080/` in your web
browser. You should see a short hello world message. If you go back to
the console where you started the application, you will probably see
no additional messages. This is because the log level is set to
WARNING as the default. Quit the application with ctrl-c and restart
it with an additional option:

```
./bin/helloworld.py --log-level-console=DEBUG
```

You will se a couple of extra messages compared to the last time. Now
visit the same URL as above in your web browser. The result should be
the same, but in the console, there are far more messages than the
last time.

Go to another terminal, and run the following command:

```
curl -i -H "Accept: application/json,*/*;q=0.5" http://localhost:8080/
```

It will hopefully produce a couple of HTTP headers as well as a JSON
hello world message. This demonstrates the content negotiation
capabilities of Guernsey. It will switch between HTML and JSON
depending on what you ask for in the Accept header.

Guernsey is by no means limited to HTML and JSON. Resource classes can
implement their own content producers which can be plugged into the
library with an associated media type. If you e.g. want to provide a
response in plain text, you can add a content producer for the
text/plain media type. More on this in a later example application.

One more thing before we conclude this document. Guernsey applications
that inherit from the `RootResource` class are automatically provided
with online help. Try running the following command:

```
./bin/helloworld.py -h
```

This should produce quite a long list of options, with associated
descriptions and default values, where applicable.
