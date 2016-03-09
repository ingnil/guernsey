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

class SimpleTemplateDemo(rest.RootResource):
    #
    # Set a few usage parameters, used by the online help system
    #
    version = "0.1"
    desc = "Simple Template Demo example application"
    usage = "Usage: %prog [OPTIONS]"

    #
    # Define a constructor for your application class, calling the RootResource constructor
    # with the appName and the appId parameters.
    #
    # appName	- Used in log messages
    # appId	- Used for the log file names
    #
    def __init__(self):
        rest.RootResource.__init__(self, appName="SimpleTemplateDemo",
                                   appId="guernsey-simple-template-demo")

    #
    # Define a getModel() method that simply returns a dictionary with
    # the key/value pairs we want to make available to the
    # user/template. In this case, we provide the title of the page as well
    # as the current date formatted according to ISO-8601.
    #
    def getModel(self):
        import datetime
        return {'title': self.appName,
                'date': str(datetime.date.today())}

    #
    # Define a getHtml() method that simply returns the template model
    # provided by the getModel() method. We could have put the code
    # directly in the getHtml() method, but we want to reuse the code
    # for the getJson() method provided in the README file.
    #
    def getHtml(self, request):
        return self.getModel()

#
# Main method
#

def main():
    app = SimpleTemplateDemo()
    app.run()
    
if __name__ == '__main__':
    main()
