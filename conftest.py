"""
Stub out the minimal Zope modules needed for pytest to import the package.

``collective/big/bang/__init__.py`` imports ``zope.i18nmessageid`` at module
level.  This conftest is loaded by pytest *before* any package is traversed,
so the stubs are in sys.modules when __init__.py runs — no Zope installation
required for unit tests.
"""
import sys
from types import ModuleType
from unittest.mock import MagicMock


def _stub(name):
    m = ModuleType(name)
    m.__spec__ = None
    return m


_stubs = {
    "zope": _stub("zope"),
    "zope.i18nmessageid": _stub("zope.i18nmessageid"),
    "zope.interface": _stub("zope.interface"),
    "zope.lifecycleevent": _stub("zope.lifecycleevent"),
}

_stubs["zope"].i18nmessageid = _stubs["zope.i18nmessageid"]
_stubs["zope.i18nmessageid"].MessageFactory = MagicMock(return_value=MagicMock())
_stubs["zope"].interface = _stubs["zope.interface"]
_stubs["zope.interface"].implementer = lambda *a, **kw: (lambda cls: cls)
_stubs["zope"].lifecycleevent = _stubs["zope.lifecycleevent"]
_stubs["zope.lifecycleevent"].IObjectModifiedEvent = MagicMock()

for _name, _mod in _stubs.items():
    sys.modules.setdefault(_name, _mod)
