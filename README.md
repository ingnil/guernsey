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

```
virtualenv venv
```

## Activate your virtual environment

```
. venv/bin/activate
```

## Install Twisted and Cheetah into the virtual environment

```
pip install twisted
pip install Cheetah
```

Note that this requires GCC. If you are using CentOS, Fedora or a
similar Linux distribution, you can just run the following command (as
root or using sudo):

```
yum groupinstall "Development Tools"
```

## Install the latest version of Guernsey into the virtual environment

```
make install-venv
```

## Deactivate your virtual environment (when you are done with it)

```
deactivate
```

If you are developing your own application using Guernsey, you only
need to create your virtual environment and install the dependencies
once. Then activate the virtual environment when developing with
Guernsey and deactivate when you want to use default Python
environment instead.

# Additional SSL/TLS requirements

If you want to use SSL/TLS, you need to install some additional
packages. Make sure that you are in your virtual environment, then
run:

```
pip install pyOpenSSL
```

If this fails, check that you have the development packages for
OpenSSL and libffi installed. For me, running CentOS 7, I had to run
the following command (as root or using sudo):

```
yum install openssl-devel libffi-devel
```

Then rerun

```
pip install pyOpenSSL
```

## Generating SSL private key and certificate

These commands generate a simple self-signed certificate that you can
use for testing. I assume that your current directory is the
application directory.

```
mkdir keys
openssl genrsa -out keys/server.key
openssl req -new -key keys/server.key -out keys/server.csr
openssl x509 -req -days 365 -in keys/server.csr -signkey keys/server.key -out keys/server.crt
```

## Running your application using SSL

Since SSL support is built into the RootResource class, if you use it
for your application, you can enable SSL with a few command-line
arguments:

### Enable SSL (required)

```
--enable-ssl 
```

### Specify SSL ports (optional)

```
--ssl-port=443 --extra-ssl-port=4433
```

### Specify SSL private key and certificate (optional)

```
--ssl-private-key=keys/server.key --ssl-certificate=keys/server.crt
```

# Example applications

Example applications are available in the examples directory. They
each have a README file as well as ample code comments.

# Credits

At the time of initial release, most of this library (excluding the
example applications) was developed for Magine Sweden AB
(http://www.magine.com/). It is released under the GNU General Public
License with their permission.
