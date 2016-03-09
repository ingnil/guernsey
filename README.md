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

# Guernsey

Web service library for Python applications built on the Twisted library

For development, I suggest using virtualenv, like this:

First, go to the Guernsey library. Then:

## Create your virtual environment

  virtualenv venv

## Activate your virtual environment

  . venv/bin/activate

## Install Twisted and Cheetah into the virtual environment

  pip install twisted
  pip install Cheetah

## Install the latest version of Guernsey into the virtual environment

  make install-venv

## Deactivate your virtual environment

  deactivate

If you are developing your own application using Guernsey, you only
need to create your virtual environment and install the dependencies
once. Then activate the virtual environment when developing with
Guernsey and deactivate when you want to use default Python
environment instead.

# Example applications

Example applications are available in the examples directory. They
each have a README file as well as ample code comments.

# Credits

At the time of initial release, most of this library (excluding the
example applications) was developed for Magine Sweden AB
(http://www.magine.com/). It is released under the GNU General Public
License with their permission.
