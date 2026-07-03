#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all pending upgrade steps for installed profiles.

Usage:
    bin/instance run scripts/upgrade_steps.py

See collective.big.bang.scripts.upgrade_steps for environment variables.
"""
from collective.big.bang.scripts.upgrade_steps import run_upgrade_steps

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("collective.big.bang.upgrade_steps")

if __name__ == "__main__":
    # 'app' is injected by 'bin/instance run'
    success = run_upgrade_steps(app)  # noqa: F821
    if success:
        logger.info("Upgrade steps completed successfully")
    else:
        logger.error("Upgrade steps failed")
