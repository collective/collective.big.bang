# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import sys
from collective.big.bang import interfaces

sys.modules['collective.big.bang.interface'] = interfaces


_ = MessageFactory("collective.big.bang")
