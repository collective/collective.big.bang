#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all pending upgrade steps for installed profiles.

This script runs all pending GenericSetup upgrade steps for all profiles
that have pending upgrades.

Usage as entry point:
    upgrade_steps /path/to/zope.conf

Usage with bin/instance run:
    bin/instance run scripts/upgrade_steps.py

Environment Variables:
    SITE_ID - Site ID in Zope (default: "Plone")
"""
from AccessControl.SecurityManagement import noSecurityManager
from collective.big.bang.big import logger
from collective.big.bang.big import setup_request
from collective.big.bang.big import setup_security
from collective.big.bang.expansion import upgrade_all_profiles

import argparse
import logging
import os
import sys


def run_upgrade_steps(app):
    """Run all pending upgrade steps for all profiles."""
    site_id = os.getenv("SITE_ID", "Plone")

    logger.info(f"Running upgrade steps for site: {site_id}")

    # Set up request
    app = setup_request(app)

    # Set up security
    if not setup_security(app):
        return False

    container = app.unrestrictedTraverse("/")

    # Check if site exists
    if site_id not in container.objectIds():
        logger.error(f"Site '{site_id}' does not exist")
        noSecurityManager()
        return False

    site = getattr(container, site_id, None)
    if site is None:
        logger.error(f"Could not get site '{site_id}'")
        noSecurityManager()
        return False

    portal_setup = site.portal_setup

    # Run all pending upgrade steps
    try:
        upgrade_all_profiles(portal_setup)
        logger.info("All upgrade steps completed successfully")
    except Exception as e:
        logger.error(f"Failed to run upgrade steps: {e}")
        noSecurityManager()
        return False

    noSecurityManager()
    return True


def main():
    """Entry point for console script."""
    parser = argparse.ArgumentParser(
        description="Run all pending upgrade steps for installed profiles"
    )
    parser.add_argument(
        "zope_conf",
        help="Path to zope.conf configuration file",
    )
    parser.add_argument(
        "-v", "--verbose",
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
        success = run_upgrade_steps(app)
        if success:
            logger.info("Upgrade steps completed successfully")
            sys.exit(0)
        else:
            logger.error("Upgrade steps failed")
            sys.exit(1)
    finally:
        app._p_jar.close()


if __name__ == "__main__":
    # When run via 'bin/instance run', 'app' is injected
    try:
        app  # noqa: F821
        # Running via bin/instance run
        logging.basicConfig(level=logging.INFO)
        success = run_upgrade_steps(app)  # noqa: F821
        if success:
            logger.info("Upgrade steps completed successfully")
        else:
            logger.error("Upgrade steps failed")
    except NameError:
        # Running as standalone script
        main()
