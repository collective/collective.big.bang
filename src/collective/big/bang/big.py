#!/usr/bin/env python
# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from collective.big.bang.event import DarwinStartedEvent
from plone.api import env
from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite
from Testing.makerequest import makerequest
from zope.component.hooks import setSite
from zope.event import notify
from zope.globalrequest import setRequest

import logging
import os
import transaction
import Zope2

logger = logging.getLogger("collective.big.bang")


def _default_packages_for_plone_version():
    plone_version = int(str(env.plone_version()[0]))
    if plone_version < 5:
        theme = "plonetheme.classic:default, plonetheme.sunburst:default"
    else:
        theme = "plonetheme.barceloneta:default"
    return "plone.app.caching:default, " + theme


def bang(event):
    is_bigbang_active = os.getenv("ACTIVE_BIGBANG", False)
    if is_bigbang_active == "True":
        app = Zope2.app()
        site_id = os.getenv("SITE_ID", "Plone")

        create_plone_site(app, site_id)

        admin_password = os.getenv("ADMIN_PASSWORD", None)
        if admin_password and getattr(app.acl_users, "users", None):
            # update zope admin password
            users = app.acl_users.users
            users.updateUserPassword("admin", admin_password)
            transaction.commit()
            logger.info("Admin password updated")

        try:
            plone = app.unrestrictedTraverse(site_id)
            notify(DarwinStartedEvent(plone))
        except KeyError as err:
            logger.info("Site not found at path " + site_id)


def create_plone_site(app, site_id):
    app = makerequest(app)
    app.REQUEST["PARENTS"] = [app]
    setRequest(app.REQUEST)
    container = app.unrestrictedTraverse("/")
    oids = container.objectIds()
    if site_id not in oids and "/" not in site_id:
        acl_users = app.acl_users
        user = acl_users.getUser("admin")
        if user:
            user = user.__of__(acl_users)
            newSecurityManager(None, user)
            logger.info("Retrieved the admin user")
        else:
            logger.error("No admin user")
            return

        # install Plone site
        extension_ids = tuple(
            [
                extension.strip()
                for extension in os.getenv(
                    "PLONE_EXTENSION_IDS", _default_packages_for_plone_version()
                ).split(",")
            ]
        )

        default_language = os.getenv("DEFAULT_LANGUAGE", "en")
        addPloneSite(
            container,
            site_id,
            title="{0} site".format(site_id),
            profile_id=_DEFAULT_PROFILE,
            extension_ids=extension_ids,
            setup_content=True,
            default_language=default_language,
        )

        plone = getattr(container, site_id)
        setSite(plone)
        noSecurityManager()
        transaction.commit()
        logger.info("Plone Site created")
    else:
        logger.info(
            "A Plone Site '{0}' already exists and will not be replaced".format(site_id)
        )
