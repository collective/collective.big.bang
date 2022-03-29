#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collective.big.bang.interface import IDarwinStartedEvent
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent


@implementer(IDarwinStartedEvent)
class DarwinStartedEvent(ObjectModifiedEvent):
    def __init__(self, object):
        super(DarwinStartedEvent, self).__init__(
            object,
            "The earth began to cool, the autotrophs began to drool. "
            "Neanderthals developed tools...",
        )
