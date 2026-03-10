#!/usr/bin/make
#
all: run

BUILDOUT_FILES = bin/buildout buildout.cfg buildout.d/*.cfg

.PHONY: buildout-6.0 buildout-6.1 cleanall test coverage test-functional coverage-full

buildout-6.0: cleanall
	python3 -m venv .
	bin/pip install -r requirements-6.0.txt
	bin/buildout -c test_plone-6.0.cfg

buildout-6.1: cleanall
	python3 -m venv .
	bin/pip install -r requirements-6.1.txt
	bin/buildout -c test_plone-6.1.cfg

test:
	uv run --with pytest pytest -v

coverage:
	uv run --with pytest --with pytest-cov pytest --cov --cov-report=term-missing --cov-report=html

test-functional:
	@echo "--- Not active ---"
	ACTIVE_BIGBANG=False PLONE_SITE=test bin/instance start && sleep 15 && bin/instance stop
	cat var/log/instance.log && rm var/log/instance.log
	bin/instance run test_scripts/did_nothing_not_active.py
	@echo "--- Active default ---"
	ACTIVE_BIGBANG=True bin/instance start && sleep 15 && ACTIVE_BIGBANG=True bin/instance stop
	cat var/log/instance.log && rm var/log/instance.log
	ACTIVE_BIGBANG=True bin/instance run test_scripts/created_default_site.py
	@echo "--- Active bad site id ---"
	ACTIVE_BIGBANG=True SITE_ID=test/Plone bin/instance start && sleep 15 && ACTIVE_BIGBANG=True SITE_ID=test/Plone bin/instance stop
	cat var/log/instance.log && rm var/log/instance.log
	ACTIVE_BIGBANG=True SITE_ID=test/Plone bin/instance run test_scripts/created_default_site.py
	@echo "--- Create custom site ---"
	ACTIVE_BIGBANG=True SITE_ID=testingsite PLONE_EXTENSION_IDS=plone.app.caching:default DEFAULT_LANGUAGE=fr bin/instance start && sleep 15 && ACTIVE_BIGBANG=True SITE_ID=testingsite bin/instance stop
	cat var/log/instance.log && rm var/log/instance.log
	ACTIVE_BIGBANG=True SITE_ID=testingsite PLONE_EXTENSION_IDS=plone.app.caching:default DEFAULT_LANGUAGE=fr bin/instance run test_scripts/created_site_with_id_and_profiles.py
	@echo "--- Update admin password ---"
	ADMIN_PASSWORD=test ACTIVE_BIGBANG=True bin/instance run test_scripts/admin_password_updated.py
	@echo "--- Admin password not updated ---"
	ADMIN_PASSWORD=test1234 ACTIVE_BIGBANG=False bin/instance run test_scripts/admin_password_not_updated.py
	@echo "--- Run all upgrade steps ---"
	ACTIVE_BIGBANG_EXPANSION=True bin/instance run test_scripts/upgrade_steps.py

coverage-full:
	bin/pip install coverage -q
	uv run --with pytest --with pytest-cov pytest --cov --cov-report= -v
	@echo "--- Not active ---"
	ACTIVE_BIGBANG=False bin/instance start && sleep 15 && bin/instance stop
	cat var/log/instance.log && rm var/log/instance.log
	bin/python -m coverage run --append bin/instance run test_scripts/did_nothing_not_active.py
	@echo "--- Active default ---"
	ACTIVE_BIGBANG=True bin/instance start && sleep 15 && ACTIVE_BIGBANG=True bin/instance stop
	cat var/log/instance.log && rm var/log/instance.log
	ACTIVE_BIGBANG=True bin/python -m coverage run --append bin/instance run test_scripts/created_default_site.py
	@echo "--- Active bad site id ---"
	ACTIVE_BIGBANG=True SITE_ID=test/Plone bin/instance start && sleep 15 && ACTIVE_BIGBANG=True SITE_ID=test/Plone bin/instance stop
	cat var/log/instance.log && rm var/log/instance.log
	ACTIVE_BIGBANG=True SITE_ID=test/Plone bin/python -m coverage run --append bin/instance run test_scripts/created_default_site.py
	@echo "--- Create custom site ---"
	ACTIVE_BIGBANG=True SITE_ID=testingsite PLONE_EXTENSION_IDS=plone.app.caching:default DEFAULT_LANGUAGE=fr bin/instance start && sleep 15 && ACTIVE_BIGBANG=True SITE_ID=testingsite bin/instance stop
	cat var/log/instance.log && rm var/log/instance.log
	ACTIVE_BIGBANG=True SITE_ID=testingsite PLONE_EXTENSION_IDS=plone.app.caching:default DEFAULT_LANGUAGE=fr bin/python -m coverage run --append bin/instance run test_scripts/created_site_with_id_and_profiles.py
	@echo "--- Update admin password ---"
	ADMIN_PASSWORD=test ACTIVE_BIGBANG=True bin/python -m coverage run --append bin/instance run test_scripts/admin_password_updated.py
	@echo "--- Admin password not updated ---"
	ADMIN_PASSWORD=test1234 ACTIVE_BIGBANG=False bin/python -m coverage run --append bin/instance run test_scripts/admin_password_not_updated.py
	@echo "--- Run all upgrade steps ---"
	ACTIVE_BIGBANG_EXPANSION=True bin/python -m coverage run --append bin/instance run test_scripts/upgrade_steps.py
	uv run --with coverage python -m coverage report --include="src/collective/big/bang/*.py"
	uv run --with coverage python -m coverage html --include="src/collective/big/bang/*.py"

cleanall:
	rm -fr bin develop-eggs lib include share .installed.cfg .mr.developer.cfg pyvenv.cfg parts downloads eggs
