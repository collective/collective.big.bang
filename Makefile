#!/usr/bin/make
#
all: run

BUILDOUT_FILES = bin/buildout buildout.cfg buildout.d/*.cfg

.PHONY: buildout-6.0 buildout-6.1 cleanall test-scripts test coverage

buildout-6.0: cleanall
	python3 -m venv .
	bin/pip install -r requirements-6.0.txt
	bin/buildout -c test_plone-6.0.cfg

buildout-6.1: cleanall
	python3 -m venv .
	bin/pip install -r requirements-6.1.txt
	bin/buildout -c test_plone-6.1.cfg

test-scripts:
	bin/python -m unittest discover -s src/collective/big/bang/tests -p "test_scripts.py" -v

test:
	bin/python -m unittest discover -s src/collective/big/bang/tests -p "test_scripts.py" -p "test_big_and_expansion.py" -v

coverage:
	bin/python -m coverage run -m unittest discover -s src/collective/big/bang/tests -p "test_scripts.py" -p "test_big_and_expansion.py"
	bin/python -m coverage report --include="src/collective/big/bang/*.py"
	bin/python -m coverage html --include="src/collective/big/bang/*.py"

cleanall:
	rm -fr bin develop-eggs lib include share .installed.cfg .mr.developer.cfg pyvenv.cfg parts downloads eggs
