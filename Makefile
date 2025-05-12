#!/usr/bin/make
#
all: run

BUILDOUT_FILES = bin/buildout buildout.cfg buildout.d/*.cfg

.PHONY: buildout-6.0 buildout-6.1 cleanall

buildout-6.0: cleanall
	python3 -m venv .
	bin/pip install -r requirements-6.0.txt
	bin/buildout -c test_plone-6.0.cfg

buildout-6.1: cleanall
	python3 -m venv .
	bin/pip install -r requirements-6.1.txt
	bin/buildout -c test_plone-6.1.cfg

cleanall:
	rm -fr bin develop-eggs lib include share .installed.cfg .mr.developer.cfg pyvenv.cfg parts downloads eggs
