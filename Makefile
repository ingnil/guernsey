#
#    Guernsey - Library to simplify creating REST web services using Python and Twisted
#    Copyright (C) 2014 Magine Sweden AB
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

SHELL:=/bin/bash
DEBDIR:=deb
TARGET:=guernsey
TARGETDIR:=$(DEBDIR)/$(TARGET)
DESTDIR:=/opt
DISTDIR:=dist/$(TARGET)
FINDCMD1=find . '(' -name '*~' -or -name '*.pyc' -or -name '*.tar.gz' -or -name '*.deb' ')'
FINDCMD2=find . -maxdepth 1 '(' -name dist -or -name deb ')'
PTHPATH=/usr/local/lib/python2.7/dist-packages
VENVDIR=venv
VENVLIBDIR=$(VENVDIR)/lib/python2.7/site-packages

.PHONY: deb dist clean list-clean

deb:
	rm -rf $(DEBDIR)
	mkdir -p $(TARGETDIR)/etc/init
	mkdir -p $(TARGETDIR)/DEBIAN
	mkdir -p $(TARGETDIR)$(DESTDIR)/lib/python/$(TARGET)
	mkdir -p $(TARGETDIR)$(PTHPATH)
	cp -R lib/python/* $(TARGETDIR)$(DESTDIR)/lib/python/$(TARGET)
	cp pkg/deb/control $(TARGETDIR)/DEBIAN/control
	echo "$(DESTDIR)/lib/python" > $(TARGETDIR)$(PTHPATH)/guernsey.pth
	cd $(DEBDIR) && fakeroot -- dpkg-deb -b $(TARGET) .
	rm -rf $(TARGETDIR)

dist:
	rm -rf dist
	mkdir -p $(DISTDIR)
	cp -R examples devel lib pkg Makefile $(DISTDIR)
	cd dist && tar zcvf $(TARGET).tar.gz $(TARGET) && rm -rf $(TARGET)

install-venv:
	rm -rf $(VENVLIBDIR)/$(TARGET)
	mkdir $(VENVLIBDIR)/$(TARGET)
	cp -R lib/python/* $(VENVLIBDIR)/$(TARGET)

clean:
	$(FINDCMD1) -delete
	$(FINDCMD2) -delete

list-clean:
	$(FINDCMD1) -ls
	$(FINDCMD2) -ls
