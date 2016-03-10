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

## Development

For development, I suggest using a virtual environment created with
virtualenv.

If you are developing your own application using Guernsey, you only
need to create your virtual environment and install the dependencies
once. Then activate the virtual environment when developing with
Guernsey and deactivate when you want to use default Python
environment instead.

### Create your virtual environment

```
virtualenv venv
```

This creates a virtual environment in a directory called `venv`
directly below your current directory.

### Activate your virtual environment

```
. venv/bin/activate
```

### Install Twisted and Cheetah into the virtual environment

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

### Install the latest version of Guernsey into the virtual environment

```
make install-venv
```

This command assumes that your current directory is the Guernsey
distribution directory, and that your virtual environment is located
in a directory called `venv` directly below the current directory.

### Deactivate your virtual environment

```
deactivate
```

This will deactivate your virtual environment for the time being,
restoring the Python environment to the default system environment. To
reactivate your virtual environment, see the activate step above.

## Additional SSL/TLS requirements

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

### Generating SSL private key and certificate

These commands generate a simple self-signed certificate that you can
use for testing. The commands below assume that your current directory
is the application directory.

```
mkdir keys
openssl genrsa -out keys/server.key
openssl req -new -key keys/server.key -out keys/server.csr
openssl x509 -req -days 365 -in keys/server.csr -signkey keys/server.key -out keys/server.crt
```

### Running your application using SSL

Since SSL support is built into the RootResource class, if you use it
for your application, you can enable SSL with a few command-line
arguments:

#### Enable SSL

```
--enable-ssl 
```

This argument is required to enable SSL/TLS.

#### Specify SSL ports

```
--ssl-port=443 --extra-ssl-port=4433
```

These arguments are optional. The default SSL port is 4433.

#### Specify SSL private key and certificate

```
--ssl-private-key=keys/server.key --ssl-certificate=keys/server.crt
```

These arguments are optional. The default private key path is
`keys/server.key` and the default certificate path is
`keys/server.crt`.

## Additional features

Most of these features requre your application to subclass the
RootResource class.

### CLI argument parsing and online help

Command-line argument parsing is provided automatically, along with a
fairly long list of CLI options already defined, with sensible
defaults. A mechanism for adding your own CLI arguments is also
available.

If you run your application with the `-h` or `--help` arguments, you
will get a list of all available arguments along with help texts.

### Logging

There is fairly comprehensive logging support available. Both file and
console loggers are available, and you can set different log levels on
them. The file logger rotates files automatically based on a maximum
file size and a maximum number of log files to keep. See the online
help for more information.

### Support for multiple port numbers

You normally specifyt the HTTP port number using the `-p` or `--port`
CLI arguments, but if you want to expose the application on additional
HTTP ports you can specify multiple instances of the `--extra-port`
argument. This might be useful e.g. if you initially deploy your
application on port 8080, but later want to switch to port 80 without
breaking possible dependencies.

### Support for Cross-Origin Resource Sharing (CORS)

If you want to allow web services running on other hosts to perform
cross-site AJAX requests to your Guernsey application, you can specify
allowed origins and request methods using the `--cors-allow-origin`
and `--cors-allow-method` arguments. Multiple instances of both these
arguments are allowed.

### Binding to privileged port numbers

If you want to expose the application on privileged port numbers such
as 80 (HTTP) and/or 443 (HTTPS), you need to start the server as
root. But to avoid the security risks of running the application as
root, you can specify a a non-privileged user and group name using the
`--user` and `--group` CLI arguments. Then the server will drop root
privileges and switch to the specified nonprivileged user after the
sockets have been bound to the privileged ports.

These two CLI arguments are invalid when starting the application as a
non-root user.

### ACME (Letsencrypt) support

By adding the command-line argument `--enable-acme`, you can enable
support for the Letsencrypt Webroot plugin (see
https://letsencrypt.org/ for more information). By running Letsencrypt
with the Webroot plugin, and specifying your template directory as the
webroot, Letsencrypt can place its challenge files in the
`.well-known` subdirectory of the template directory. This allows it
to validate ownership of your domain and automatically issue an SSL
certificate without server downtime.

This requires the server to be bound to the default (privileged) port
numbers of 80 for HTTP and/or 443 for HTTPS. In order to do this, you
need to start the server as root, but see the above section about
running as a non-privileged user.

### Support for (web-based) online reconfiguration of certain variables

If you visit the `[PROTOCOL]://[SERVER_ADDRESS]:[SERVER_PORT]/config/`
URL, it is possible to change some variables in the server
configuration. By default, this only includes the file logging level
and the file logging format string, but it can be extended by the
application.

## Example applications

Example applications are available in the `examples` directory. They
each have a `README` file as well as ample code comments.

## Credits

At the time of initial release, most of this library (excluding the
example applications) was developed for Magine Sweden AB
(http://www.magine.com/). It is released under the GNU General Public
License with their permission.
