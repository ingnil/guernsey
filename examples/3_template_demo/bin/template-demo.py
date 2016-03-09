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
# Import the Guernsey REST library and the Guernsey model library
#

import guernsey.web.rest as rest
import guernsey.web.model as gwm

#
# Create a model class for cities, inheriting from the Guernsey Model
# class. This class provides a few convenience methods that can be
# useful when dealing with models, such as e.g. a __repr__()
# method. When initialized with a dictionary, it also creates and sets
# attributes for each of the key/value pairs in the supplied
# dictionary. Finally, it also sets up a logger for the class.
#

class CityModel(gwm.Model):
    name = None
    country = None

#
# Create a resource class for cities. This class is responsible for
# all requests to the cities resource, and takes care of producing
# HTML, JSON and possibly other formats that you want to supply (in
# this case, we add a producer for the CSV format).
#

class CitiesResource(rest.Resource):
    def __init__(self, parent):
        rest.Resource.__init__(self, parent)
        self.addContentTypeProducer("text/csv", self.getCsv)
        
        #
        # Common method to create a model that depending on the format
        # can either be supplied directly to the user, or tailored by
        # the format producers to suit its specific needs.
        #
        # The database in this case is only there for show. This
        # collection could just as well have been delivered from a
        # real database server, although to avoid blocking the
        # reactor, it would have to involve threading and deferred
        # replies. More on that later.
        #

    def getModel(self):
        database = {"Stockholm": "Sweden",
                    "Helsinki": "Finland",
                    "Copenhagen": "Denmark",
                    "Oslo": "Norway"}
        cities = {}
        for city, country in database.iteritems():
            cities[city] = CityModel({"name": city,
                                      "country": country})
        return cities

    #
    # We process the model slightly to suit our HTML template.
    #
    def getHtml(self, request):
        cities = []
        for city in sorted(self.getModel().itervalues(), key=lambda x: x.name):
            cities.append(city)
        return {"cities": cities}

    #
    # The JSON producer returns the model directly, since the
    # framework takes care of converting the model to JSON
    #
    def getJson(self, request):
        return self.getModel()

    #
    # Only getHtml() uses templates by default. Other producers except
    # the JSON producer have to return a string, but they could of
    # course use the templating framework directly, e.g. by calling
    # the fillTemplate() method in the Guernsey Resource class.
    #
    def getCsv(self, request):
        cities = []
        for city in sorted(self.getModel().itervalues(), key=lambda x: x.name):
            cities.append("%s,%s" % (city.name, city.country))
        return "\n".join(cities) + "\n"

#
# Create your application class, inheriting from the Guernsey RootResource class
#

class TemplateDemo(rest.RootResource):
    #
    # Set a few usage parameters, used by the online help system
    #
    version = "0.1"
    desc = "Slightly more complex templating example application"
    usage = "Usage: %prog [OPTIONS]"

    #
    # Define a constructor for your application class, calling the
    # RootResource constructor in turn. Then add an instance of the
    # CitiesResource class as a child resource.
    #
    def __init__(self):
        rest.RootResource.__init__(self, appName="TemplateDemo",
                                   appId="guernsey-template-demo")
        self.putChild("cities", CitiesResource(self))
        
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
    # provided by the getModel() method.
    #
    def getHtml(self, request):
        return self.getModel()

    #
    # Define a getJson() method that simply returns the template model
    # provided by the getModel() method.
    #
    def getJson(self, request):
        return self.getModel()

#
# Main method
#

def main():
    app = TemplateDemo()
    app.run()
    
if __name__ == '__main__':
    main()
