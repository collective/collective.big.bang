#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zope.lifecycleevent import IObjectModifiedEvent


class IDarwinStartedEvent(IObjectModifiedEvent):
    """
    Site is created an admin password updated.
    """
