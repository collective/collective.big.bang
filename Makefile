#!/usr/bin/make
#
all: run

BUILDOUT_FILES = bin/buildout buildout.cfg buildout.d/*.cfg

.PHONY: buildout-4.3 buildout-5.1 buildout-5.2 buildout-6.0 cleanall

buildout-4.3: cleanall
	virtualenv -p python2 .
	bin/pip install -r requirements-4.3.txt
	bin/buildout -c test_plone-4.3.cfg

buildout-5.1: cleanall
	virtualenv -p python2 .
	bin/pip install -r requirements-5.1.txt
	bin/buildout -c test_plone-5.1.cfg

buildout-5.2: cleanall
	virtualenv .
	bin/pip install -r requirements-5.2.txt
	bin/buildout -c test_plone-5.2.cfg

buildout-6.0: cleanall
	virtualenv .
	bin/pip install -r requirements-6.0.txt
	bin/buildout -c test_plone-6.0.cfg

cleanall:
	rm -fr bin develop-eggs lib include share .installed.cfg .mr.developer.cfg pyvenv.cfg parts downloads eggs
