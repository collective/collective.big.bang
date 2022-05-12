#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zope.lifecycleevent import IObjectModifiedEvent


class IDarwinStartedEvent(IObjectModifiedEvent):
    """
    After site is created and admin password updated.
    """
