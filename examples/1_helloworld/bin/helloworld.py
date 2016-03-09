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

#
# Import the Guernsey REST library
#

import guernsey.web.rest as rest

#
# Create your application class, inheriting from the Guernsey RootResource class
#

class HelloWorld(rest.RootResource):
    #
    # Set a few usage parameters, used by the online help system
    #
    version = "0.1"
    desc = "Hello World example application"
    usage = "Usage: %prog [OPTIONS]"

    #
    # Define a constructor for your application class, calling the RootResource constructor
    # with the appName and the appId parameters.
    #
    # appName	- Used in log messages
    # appId	- Used for the log file names
    #
    def __init__(self):
        rest.RootResource.__init__(self, appName="HelloWorld", appId="guernsey-helloworld")

    #
    # Define a very simple getHtml() method, using the one from the Resource class. The
    # RootResource class has its own version of this method, but that one requires a
    # template to be available, so we override that method for now.
    #
    def getHtml(self, request):
        return rest.Resource.getHtml(self, request)

#
# Main method
#

def main():
    app = HelloWorld()
    app.run()
    
if __name__ == '__main__':
    main()
