.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://img.shields.io/pypi/v/collective.big.bang.svg
    :target: https://pypi.python.org/pypi/collective.big.bang/
    :alt: Latest Version

.. image:: https://github.com/collective/collective.big.bang/actions/workflows/test.yml/badge.svg
    :target: https://github.com/collective/collective.big.bang/actions/workflows/test.yml
    :alt: Tests Status

.. image:: https://img.shields.io/pypi/pyversions/collective.big.bang.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.big.bang.svg
    :target: https://pypi.python.org/pypi/collective.big.bang/
    :alt: License


===================
collective.big.bang
===================
::

    Our whole universe was in a hot, dense state
    Then nearly fourteen billion years ago expansion started, wait
    The earth began to cool, the autotrophs began to drool
    Neanderthals developed tools
    We built a wall (we built the pyramids)
    Math, science, history, unraveling the mysteries
    That all started with the big bang! Hey!

So all started with the Plone site! Hey!
This package it used to create Plone site when Zope is started (just before `Ready to handle requests` sentence).

You can use environment variables to create Plone site and choose package you would like to install. See "Environment variables"


Why not use collective.recipe.plonesite?
The goal is to create Plone site when you deploy a new Plone on a contenerized env.
We think it's easy to create Plone site when you start it without entrypoint or without using and other command.
It's more simple in a contenerized environment that starting a buildout part to create a Pone site.



Fun fact:

This package is now called collective.big.bang instead of the original collective.bigbang, because collective.bigbang name was rejected by pypi naming package.


.. _Environment variables:

Environment variables
---------------------
You can add environment variable into your buildout in instance part with "environment-vars"::

    ...
    [instance]
    ...
    environment-vars =
        PLONE_EXTENSION_IDS plone.app.caching:default,plonetheme.barceloneta:default
        DEFAULT_LANGUAGE fr
        ADMIN_PASSWORD mysuperpa$$w0rd
        ACTIVE_BIGBANG True
    ...

Or you can also use tools like `direnv <https://direnv.net/>`_ (.envrc file example)::

    export PLONE_EXTENSION_IDS=plone.app.caching:default,plonetheme.barceloneta:default
    export DEFAULT_LANGUAGE=fr
    export ADMIN_PASSWORD=mysuperpa$$w0rd
    export ACTIVE_BIGBANG=True


PLONE_EXTENSION_IDS
    A list of GenericSetup profiles to install.
    Default values are ``plone.app.caching:default,plonetheme.barceloneta:default``

DEFAULT_LANGUAGE
    The default language of the Plone site.
    Default value is ``en``

ADMIN_PASSWORD
    The password for the zope "admin" user.
    There is no default value, if variable is not set, admin password will not be updated.

ACTIVE_BIGBANG
    Create a Plone site on this instance. This variable is used to avoid conflict error, this variable should be set to True to only one instance
    Default value is ``False``


Features
--------

- Create Plone site when Zope is started


Installation
------------

Install collective.big.bang by adding it to your buildout::

    [buildout]

    ...

    eggs +=
        collective.big.bang

    ...

    [instance]
    ...
    environment-vars =
        PLONE_EXTENSION_IDS plone.app.caching:default,plonetheme.barceloneta:default
        DEFAULT_LANGUAGE fr
        ADMIN_PASSWORD mysuperpa$$w0rd
        ACTIVE_BIGBANG True



and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.big.bang/issues
- Source Code: https://github.com/collective/collective.big.bang


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: devs@imio.be


License
-------

The project is licensed under the GPLv2.
