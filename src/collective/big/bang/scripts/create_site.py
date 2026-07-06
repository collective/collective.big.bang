#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plone site creation script using plone.distribution.api.

This is an alternative to the event-based creation in big.py,
using environment variables for configuration.

Usage as entry point:
    create_site /path/to/zope.conf

Usage with bin/instance run:
    bin/instance run scripts/create_site.py

Environment Variables:
    DISTRIBUTION       - Distribution name (default: "classic")
    SITE_ID           - Site ID in Zope (default: "Plone")
    DEFAULT_LANGUAGE  - Default language code (default: "en")
    SETUP_CONTENT     - Create example content (default: "True")
    TIMEZONE          - Portal timezone (default: "Europe/Brussels")
    DELETE_EXISTING   - Delete existing site if present (default: "False")
    ADDITIONAL_PROFILES - Comma-separated GenericSetup profiles to install
    ADMIN_PASSWORD    - Password for Zope admin user (optional)
"""
from AccessControl.SecurityManagement import noSecurityManager
from collective.big.bang.big import apply_additional_profiles
from collective.big.bang.big import delete_site
from collective.big.bang.big import ensure_admin_user
from collective.big.bang.big import get_bool_env
from collective.big.bang.big import logger
from collective.big.bang.big import setup_request
from collective.big.bang.big import setup_security
from collective.big.bang.big import update_admin_password
from zope.component.hooks import setSite

import argparse
import logging
import os
import sys
import transaction


def create_site(app):
    """Create a Plone site using plone.distribution.api."""
    from plone.distribution.api import site as site_api

    # Read configuration from environment variables
    distribution = os.getenv("DISTRIBUTION", "classic")
    site_id = os.getenv("SITE_ID", "Plone")
    default_language = os.getenv("DEFAULT_LANGUAGE", "en")
    setup_content = get_bool_env("SETUP_CONTENT", True)
    timezone = os.getenv("TIMEZONE", "Europe/Brussels")
    delete_existing = get_bool_env("DELETE_EXISTING", False)
    additional_profiles = os.getenv("ADDITIONAL_PROFILES", "")

    logger.info(f"Creating site with distribution: {distribution}")
    logger.info(f"Site ID: {site_id}")
    logger.info(f"Language: {default_language}, Timezone: {timezone}")
    logger.info(f"Setup content: {setup_content}")

    # Set up request
    app = setup_request(app)

    # Ensure admin user exists (handles fresh Data.fs after reset)
    ensure_admin_user(app)

    # Set up security
    if not setup_security(app):
        return False

    container = app.unrestrictedTraverse("/")

    # Handle existing site
    if site_id in container.objectIds():
        if delete_existing:
            delete_site(container, site_id)
        else:
            logger.info(
                f"Site '{site_id}' already exists; nothing to do. "
                "Set DELETE_EXISTING=True to replace it."
            )
            noSecurityManager()
            # Idempotent no-op: an existing site is a success, not a failure.
            # This lets the k8s create-site Job re-run safely on every deploy.
            return True

    # Build answers dict for plone.distribution.api
    answers = {
        "site_id": site_id,
        "title": f"{site_id} site",
        "description": "",
        "default_language": default_language,
        "portal_timezone": timezone,
        "setup_content": setup_content,
    }

    # Create site using plone.distribution.api
    try:
        site = site_api._create_site(
            context=container,
            distribution_name=distribution,
            answers=answers,
        )
        logger.info(f"Site created successfully: {site_id}")
    except Exception as e:
        logger.error(f"Failed to create site: {e}")
        noSecurityManager()
        return False

    # Set site hook
    setSite(site)

    # Apply additional profiles
    if additional_profiles:
        apply_additional_profiles(site, additional_profiles)

    # Update admin password if specified
    update_admin_password(app)

    # Commit transaction
    transaction.commit()
    logger.info("Transaction committed")

    noSecurityManager()
    return True


def main():
    """Entry point for console script."""
    parser = argparse.ArgumentParser(
        description="Create a Plone site using plone.distribution.api"
    )
    parser.add_argument(
        "zope_conf",
        help="Path to zope.conf configuration file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Check if zope.conf exists
    if not os.path.exists(args.zope_conf):
        logger.error(f"zope.conf not found: {args.zope_conf}")
        sys.exit(1)

    # Initialize Zope
    try:
        from Zope2.Startup.run import configure_wsgi

        configure_wsgi(args.zope_conf)
    except ImportError:
        # Fallback for older Zope versions
        from Zope2 import configure

        configure(args.zope_conf)

    import Zope2

    app = Zope2.app()

    try:
        success = create_site(app)
        if success:
            logger.info("Site creation completed successfully")
            sys.exit(0)
        else:
            logger.error("Site creation failed")
            sys.exit(1)
    finally:
        app._p_jar.close()


if __name__ == "__main__":
    # When run via 'bin/instance run', 'app' is injected
    try:
        app  # noqa: F821
        # Running via bin/instance run
        logging.basicConfig(level=logging.INFO)
        success = create_site(app)  # noqa: F821
        if success:
            logger.info("Site creation completed successfully")
        else:
            logger.error("Site creation failed")
    except NameError:
        # Running as standalone script
        main()
