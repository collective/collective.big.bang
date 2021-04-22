.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://img.shields.io/pypi/v/collective.bigbang.svg
    :target: https://pypi.python.org/pypi/collective.bigbang/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.bigbang.svg
    :target: https://pypi.python.org/pypi/collective.bigbang
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.bigbang.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.bigbang.svg
    :target: https://pypi.python.org/pypi/collective.bigbang/
    :alt: License


==================
collective.bigbang
==================
::

    Our whole universe was in a hot, dense state
    Then nearly fourteen billion years ago expansion started, wait
    The earth began to cool, the autotrophs began to drool
    Neanderthals developed tools
    We built a wall (we built the pyramids)
    Math, science, history, unraveling the mysteries
    That all started with the big bang! Hey!

So all started with the Plone site! Hey!
This package it used to create Plone site when Zope is started (just before "Ready to handle requests" sentence).

You can use environment variables to create Plone site and choose package you would like to install. See :ref:`Environment variables`


Why not use collective.recipe.plonesite?
The goal is to create Plone site when you deploy a new Plone on a contenerized env.
We think it's easy to create Plone site when you start it without entrypoint or without using and other command.
It's more simple in a contenerized environment that starting a buildout part to create a Pone site.


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
    ...

Or you can also use tools like `direnv <https://direnv.net/>`_ (.envrc file example)::

    export PLONE_EXTENSION_IDS=plone.app.caching:default,plonetheme.barceloneta:default
    export DEFAULT_LANGUAGE=fr
    export ADMIN_PASSWORD=mysuperpa$$w0rd


PLONE_EXTENSION_IDS
    A list of GenericSetup profiles to install.
    Default values are ``plone.app.caching:default,plonetheme.barceloneta:default``

DEFAULT_LANGUAGE
    The default language of the Plone site.
    Default value is ``en``

ADMIN_PASSWORD
    The password for the zope "admin" user.
    Default value is ``admin``


Features
--------

- Create Plone site when Zope is started


Installation
------------

Install collective.bigbang by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.bigbang


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.bigbang/issues
- Source Code: https://github.com/collective/collective.bigbang


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: devs@imio.be


License
-------

The project is licensed under the GPLv2.