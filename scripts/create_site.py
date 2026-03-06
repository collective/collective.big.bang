#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plone site creation script using plone.distribution.api.

Usage:
    bin/instance run scripts/create_site.py

See collective.big.bang.scripts.create_site for environment variables.
"""
from collective.big.bang.scripts.create_site import create_site

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("collective.big.bang.create_site")

if __name__ == "__main__":
    # 'app' is injected by 'bin/instance run'
    success = create_site(app)  # noqa: F821
    if success:
        logger.info("Site creation completed successfully")
    else:
        logger.error("Site creation failed")
