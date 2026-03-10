# -*- coding: utf-8 -*-
"""Unit tests for create_site and upgrade_steps entry point scripts.

These tests use unittest.mock to stub all Zope/Plone dependencies so that no
running Zope/Plone instance is needed.

Strategy
--------
A comprehensive set of stub modules is injected into sys.modules via
``patch.dict`` in ``setUpClass``.  The script module under test is imported
*inside* ``setUpClass`` (while the stubs are active) so that:

  1. All heavy third-party imports are satisfied by stubs.
  2. The module object is in sys.modules before ``@patch`` decorators try to
     resolve it (decorators resolve at test-call time, not definition time, but
     they do so *before* the test body runs).
"""
import importlib.util
import os
import sys
import unittest
from types import ModuleType
from unittest.mock import MagicMock, patch

# Directory containing the script modules under test.
_SCRIPTS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "scripts")
)


def _load_script(module_name, filename):
    """Load a script module directly from its file path, bypassing package discovery."""
    file_path = os.path.join(_SCRIPTS_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Real tiny helper (no Zope deps) used in stubs
# ---------------------------------------------------------------------------

def _get_bool_env(name, default):
    value = os.getenv(name, str(default))
    return value.lower() in ("true", "1", "yes")


# ---------------------------------------------------------------------------
# Stub-module factory helpers
# ---------------------------------------------------------------------------

def _mod(name):
    m = ModuleType(name)
    m.__spec__ = None
    return m


# ---------------------------------------------------------------------------
# Build the sys.modules stub dict
# ---------------------------------------------------------------------------

def _build_stubs():  # noqa: C901
    s = {}

    # ---- zope namespace ----
    for name in [
        "zope",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.lifecycleevent",
        "zope.component",
        "zope.component.hooks",
        "zope.event",
        "zope.globalrequest",
    ]:
        s[name] = _mod(name)

    s["zope"].i18nmessageid = s["zope.i18nmessageid"]
    s["zope.i18nmessageid"].MessageFactory = MagicMock(return_value=MagicMock())
    s["zope"].interface = s["zope.interface"]
    s["zope.interface"].implementer = lambda *a, **kw: (lambda cls: cls)
    s["zope"].lifecycleevent = s["zope.lifecycleevent"]
    s["zope.lifecycleevent"].IObjectModifiedEvent = MagicMock()
    s["zope.lifecycleevent"].ObjectModifiedEvent = object
    s["zope"].component = s["zope.component"]
    s["zope.component"].hooks = s["zope.component.hooks"]
    s["zope.component.hooks"].setSite = MagicMock()
    s["zope"].event = s["zope.event"]
    s["zope.event"].notify = MagicMock()
    s["zope"].globalrequest = s["zope.globalrequest"]
    s["zope.globalrequest"].setRequest = MagicMock()

    # ---- AccessControl ----
    s["AccessControl"] = _mod("AccessControl")
    s["AccessControl.SecurityManagement"] = _mod("AccessControl.SecurityManagement")
    s["AccessControl"].SecurityManagement = s["AccessControl.SecurityManagement"]
    s["AccessControl.SecurityManagement"].newSecurityManager = MagicMock()
    s["AccessControl.SecurityManagement"].noSecurityManager = MagicMock()

    # ---- plone ----
    for name in [
        "plone",
        "plone.api",
        "plone.api.env",
        "plone.distribution",
        "plone.distribution.api",
        "plone.distribution.api.site",
    ]:
        s[name] = _mod(name)

    s["plone"].api = s["plone.api"]
    s["plone.api"].env = s["plone.api.env"]
    s["plone"].distribution = s["plone.distribution"]
    s["plone.distribution"].api = s["plone.distribution.api"]
    s["plone.distribution.api"].site = s["plone.distribution.api.site"]
    s["plone.distribution.api.site"]._create_site = MagicMock()

    # ---- Products ----
    for name in [
        "Products",
        "Products.CMFPlone",
        "Products.CMFPlone.factory",
        "Products.Five",
        "Products.Five.browser",
        "Products.GenericSetup",
        "Products.GenericSetup.upgrade",
    ]:
        s[name] = _mod(name)

    s["Products"].CMFPlone = s["Products.CMFPlone"]
    s["Products.CMFPlone"].factory = s["Products.CMFPlone.factory"]
    s["Products.CMFPlone.factory"]._DEFAULT_PROFILE = "default"
    s["Products.CMFPlone.factory"].addPloneSite = MagicMock()
    s["Products"].Five = s["Products.Five"]
    s["Products.Five"].browser = s["Products.Five.browser"]
    s["Products"].GenericSetup = s["Products.GenericSetup"]
    s["Products.GenericSetup"].upgrade = s["Products.GenericSetup.upgrade"]
    s["Products.GenericSetup.upgrade"]._upgrade_registry = MagicMock()

    # ---- Testing ----
    s["Testing"] = _mod("Testing")
    s["Testing.makerequest"] = _mod("Testing.makerequest")
    s["Testing"].makerequest = s["Testing.makerequest"]
    s["Testing.makerequest"].makerequest = MagicMock(side_effect=lambda app: app)

    # ---- transaction ----
    s["transaction"] = _mod("transaction")
    s["transaction"].commit = MagicMock()

    # ---- Zope2 ----
    s["Zope2"] = _mod("Zope2")
    s["Zope2.Startup"] = _mod("Zope2.Startup")
    s["Zope2.Startup.run"] = _mod("Zope2.Startup.run")
    s["Zope2"].Startup = s["Zope2.Startup"]
    s["Zope2.Startup"].run = s["Zope2.Startup.run"]
    s["Zope2.Startup.run"].configure_wsgi = MagicMock()

    # ---- collective namespace (required so __import__('collective') works) ----
    s["collective"] = _mod("collective")
    s["collective"].__path__ = []
    s["collective"].__package__ = "collective"

    s["collective.big"] = _mod("collective.big")
    s["collective.big"].__path__ = []
    s["collective.big"].__package__ = "collective.big"
    s["collective"].big = s["collective.big"]

    # ---- collective.big.bang package stubs ----
    cbg = _mod("collective.big.bang")
    cbg.__path__ = []
    cbg.__package__ = "collective.big.bang"
    s["collective.big"].bang = cbg
    s["collective.big.bang"] = cbg

    cbg_ifaces = _mod("collective.big.bang.interfaces")
    cbg_ifaces.IDarwinStartedEvent = MagicMock()
    cbg.interfaces = cbg_ifaces
    s["collective.big.bang.interfaces"] = cbg_ifaces

    cbg_event = _mod("collective.big.bang.event")
    cbg_event.DarwinStartedEvent = MagicMock()
    cbg.event = cbg_event
    s["collective.big.bang.event"] = cbg_event

    cbg_big = _mod("collective.big.bang.big")
    cbg_big.setup_request = MagicMock(side_effect=lambda app: app)
    cbg_big.setup_security = MagicMock(return_value=True)
    cbg_big.delete_site = MagicMock()
    cbg_big.apply_additional_profiles = MagicMock()
    cbg_big.update_admin_password = MagicMock()
    cbg_big.get_bool_env = _get_bool_env  # real implementation, respects os.environ
    cbg_big.logger = MagicMock()
    cbg.big = cbg_big
    s["collective.big.bang.big"] = cbg_big

    cbg_expansion = _mod("collective.big.bang.expansion")
    cbg_expansion.upgrade_all_profiles = MagicMock()
    cbg.expansion = cbg_expansion
    s["collective.big.bang.expansion"] = cbg_expansion

    cbg_scripts = _mod("collective.big.bang.scripts")
    cbg_scripts.__path__ = []
    cbg_scripts.__package__ = "collective.big.bang.scripts"
    cbg.scripts = cbg_scripts
    s["collective.big.bang.scripts"] = cbg_scripts

    return s


_STUBS = _build_stubs()

_CREATE_SITE_MOD = "collective.big.bang.scripts.create_site"
_UPGRADE_STEPS_MOD = "collective.big.bang.scripts.upgrade_steps"


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

def _make_app_mock(object_ids=None):
    """Return (mock_app, mock_container) with container.objectIds() preset."""
    if object_ids is None:
        object_ids = []
    app = MagicMock(name="app")
    container = MagicMock(name="container")
    container.objectIds.return_value = object_ids
    app.unrestrictedTraverse.return_value = container
    return app, container


def _make_zope2_mock():
    """Return a minimal Zope2 stub and the app object it produces."""
    zope2 = MagicMock(name="Zope2")
    mock_app = MagicMock(name="zope_app")
    mock_app._p_jar = MagicMock()
    zope2.app.return_value = mock_app
    return zope2, mock_app


# ---------------------------------------------------------------------------
# Tests for create_site script
# ---------------------------------------------------------------------------

class TestCreateSite(unittest.TestCase):
    """Tests for collective.big.bang.scripts.create_site."""

    @classmethod
    def setUpClass(cls):
        # Activate stubs first, THEN load the module under test from file.
        cls._patcher = patch.dict(sys.modules, _STUBS)
        cls._patcher.start()
        sys.modules.pop(_CREATE_SITE_MOD, None)
        cls.mod = _load_script(_CREATE_SITE_MOD, "create_site.py")

    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()
        sys.modules.pop(_CREATE_SITE_MOD, None)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def setUp(self):
        # Reset shared MagicMocks between tests.
        _STUBS["transaction"].commit.reset_mock()
        _STUBS["zope.component.hooks"].setSite.reset_mock()
        _STUBS["collective.big.bang.big"].setup_request.reset_mock()
        _STUBS["collective.big.bang.big"].setup_security.reset_mock()
        _STUBS["collective.big.bang.big"].delete_site.reset_mock()
        _STUBS["collective.big.bang.big"].apply_additional_profiles.reset_mock()
        _STUBS["collective.big.bang.big"].update_admin_password.reset_mock()
        _STUBS["plone.distribution.api.site"]._create_site = MagicMock()

    # ------------------------------------------------------------------
    # create_site() – happy path
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.create_site.update_admin_password")
    @patch("collective.big.bang.scripts.create_site.apply_additional_profiles")
    @patch("collective.big.bang.scripts.create_site.setSite")
    @patch("collective.big.bang.scripts.create_site.noSecurityManager")
    @patch("collective.big.bang.scripts.create_site.transaction")
    @patch("collective.big.bang.scripts.create_site.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.create_site.setup_request")
    def test_success(
        self,
        mock_setup_request,
        mock_setup_security,
        mock_transaction,
        mock_no_sec,
        mock_set_site,
        mock_apply_profiles,
        mock_update_password,
    ):
        """Site absent → created, transaction committed, returns True."""
        app, _container = _make_app_mock(object_ids=[])
        mock_setup_request.return_value = app

        mock_site = MagicMock(name="new_site")
        _STUBS["plone.distribution.api.site"]._create_site = MagicMock(
            return_value=mock_site
        )

        result = self.mod.create_site(MagicMock())

        self.assertTrue(result)
        mock_transaction.commit.assert_called_once()
        mock_set_site.assert_called_once_with(mock_site)
        mock_no_sec.assert_called_once()

    # ------------------------------------------------------------------
    # create_site() – site already exists, DELETE_EXISTING=False
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.create_site.noSecurityManager")
    @patch("collective.big.bang.scripts.create_site.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.create_site.setup_request")
    def test_site_exists_no_delete(
        self, mock_setup_request, mock_setup_security, mock_no_sec
    ):
        """Site present + DELETE_EXISTING=False → returns False, no creation."""
        app, _container = _make_app_mock(object_ids=["Plone"])
        mock_setup_request.return_value = app

        _create_site_spy = MagicMock()
        _STUBS["plone.distribution.api.site"]._create_site = _create_site_spy

        with patch.dict(os.environ, {"SITE_ID": "Plone", "DELETE_EXISTING": "False"}):
            result = self.mod.create_site(MagicMock())

        self.assertFalse(result)
        _create_site_spy.assert_not_called()

    # ------------------------------------------------------------------
    # create_site() – site already exists, DELETE_EXISTING=True
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.create_site.update_admin_password")
    @patch("collective.big.bang.scripts.create_site.apply_additional_profiles")
    @patch("collective.big.bang.scripts.create_site.setSite")
    @patch("collective.big.bang.scripts.create_site.noSecurityManager")
    @patch("collective.big.bang.scripts.create_site.transaction")
    @patch("collective.big.bang.scripts.create_site.delete_site")
    @patch("collective.big.bang.scripts.create_site.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.create_site.setup_request")
    def test_site_exists_with_delete(
        self,
        mock_setup_request,
        mock_setup_security,
        mock_delete_site,
        mock_transaction,
        mock_no_sec,
        mock_set_site,
        mock_apply_profiles,
        mock_update_password,
    ):
        """Site present + DELETE_EXISTING=True → existing site deleted, new created."""
        app, container = _make_app_mock(object_ids=["Plone"])
        mock_setup_request.return_value = app

        mock_site = MagicMock(name="new_site")
        _STUBS["plone.distribution.api.site"]._create_site = MagicMock(
            return_value=mock_site
        )

        with patch.dict(os.environ, {"SITE_ID": "Plone", "DELETE_EXISTING": "True"}):
            result = self.mod.create_site(MagicMock())

        self.assertTrue(result)
        mock_delete_site.assert_called_once_with(container, "Plone")

    # ------------------------------------------------------------------
    # create_site() – setup_security returns False
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.create_site.setup_security", return_value=False)
    @patch("collective.big.bang.scripts.create_site.setup_request")
    def test_security_fails(self, mock_setup_request, mock_setup_security):
        """setup_security=False → returns False, container never touched."""
        app, _ = _make_app_mock()
        mock_setup_request.return_value = app

        result = self.mod.create_site(MagicMock())

        self.assertFalse(result)
        app.unrestrictedTraverse.assert_not_called()

    # ------------------------------------------------------------------
    # create_site() – _create_site raises
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.create_site.noSecurityManager")
    @patch("collective.big.bang.scripts.create_site.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.create_site.setup_request")
    def test_creation_exception(
        self, mock_setup_request, mock_setup_security, mock_no_sec
    ):
        """_create_site raises → logs error, returns False."""
        app, _container = _make_app_mock(object_ids=[])
        mock_setup_request.return_value = app

        _STUBS["plone.distribution.api.site"]._create_site = MagicMock(
            side_effect=RuntimeError("boom")
        )

        result = self.mod.create_site(MagicMock())

        self.assertFalse(result)
        mock_no_sec.assert_called_once()

    # ------------------------------------------------------------------
    # create_site() – ADDITIONAL_PROFILES env var
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.create_site.update_admin_password")
    @patch("collective.big.bang.scripts.create_site.apply_additional_profiles")
    @patch("collective.big.bang.scripts.create_site.setSite")
    @patch("collective.big.bang.scripts.create_site.noSecurityManager")
    @patch("collective.big.bang.scripts.create_site.transaction")
    @patch("collective.big.bang.scripts.create_site.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.create_site.setup_request")
    def test_with_additional_profiles(
        self,
        mock_setup_request,
        mock_setup_security,
        mock_transaction,
        mock_no_sec,
        mock_set_site,
        mock_apply_profiles,
        mock_update_password,
    ):
        """ADDITIONAL_PROFILES set → apply_additional_profiles called with site."""
        app, _container = _make_app_mock(object_ids=[])
        mock_setup_request.return_value = app

        mock_site = MagicMock(name="new_site")
        _STUBS["plone.distribution.api.site"]._create_site = MagicMock(
            return_value=mock_site
        )

        with patch.dict(os.environ, {"ADDITIONAL_PROFILES": "my.package:default"}):
            result = self.mod.create_site(MagicMock())

        self.assertTrue(result)
        mock_apply_profiles.assert_called_once_with(mock_site, "my.package:default")

    # ------------------------------------------------------------------
    # create_site() – update_admin_password always called
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.create_site.update_admin_password")
    @patch("collective.big.bang.scripts.create_site.apply_additional_profiles")
    @patch("collective.big.bang.scripts.create_site.setSite")
    @patch("collective.big.bang.scripts.create_site.noSecurityManager")
    @patch("collective.big.bang.scripts.create_site.transaction")
    @patch("collective.big.bang.scripts.create_site.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.create_site.setup_request")
    def test_update_admin_password_called(
        self,
        mock_setup_request,
        mock_setup_security,
        mock_transaction,
        mock_no_sec,
        mock_set_site,
        mock_apply_profiles,
        mock_update_password,
    ):
        """update_admin_password is always invoked after successful site creation."""
        app, _container = _make_app_mock(object_ids=[])
        mock_setup_request.return_value = app

        mock_site = MagicMock(name="new_site")
        _STUBS["plone.distribution.api.site"]._create_site = MagicMock(
            return_value=mock_site
        )

        self.mod.create_site(MagicMock())

        mock_update_password.assert_called_once_with(app)

    # ------------------------------------------------------------------
    # main()
    # ------------------------------------------------------------------

    def test_main_conf_not_found(self):
        """main() exits 1 when zope.conf path does not exist."""
        with patch("sys.argv", ["create_site", "/nonexistent/zope.conf"]):
            with patch("os.path.exists", return_value=False):
                with self.assertRaises(SystemExit) as cm:
                    self.mod.main()
        self.assertEqual(cm.exception.code, 1)

    def test_main_success(self):
        """main() exits 0 when create_site returns True."""
        zope2_mock, _ = _make_zope2_mock()
        with patch("sys.argv", ["create_site", "/path/to/zope.conf"]):
            with patch("os.path.exists", return_value=True):
                with patch.dict(sys.modules, {"Zope2": zope2_mock}):
                    with patch.object(self.mod, "create_site", return_value=True):
                        with self.assertRaises(SystemExit) as cm:
                            self.mod.main()
        self.assertEqual(cm.exception.code, 0)

    def test_main_failure(self):
        """main() exits 1 when create_site returns False."""
        zope2_mock, _ = _make_zope2_mock()
        with patch("sys.argv", ["create_site", "/path/to/zope.conf"]):
            with patch("os.path.exists", return_value=True):
                with patch.dict(sys.modules, {"Zope2": zope2_mock}):
                    with patch.object(self.mod, "create_site", return_value=False):
                        with self.assertRaises(SystemExit) as cm:
                            self.mod.main()
        self.assertEqual(cm.exception.code, 1)


# ---------------------------------------------------------------------------
# Tests for upgrade_steps script
# ---------------------------------------------------------------------------

class TestRunUpgradeSteps(unittest.TestCase):
    """Tests for collective.big.bang.scripts.upgrade_steps."""

    @classmethod
    def setUpClass(cls):
        cls._patcher = patch.dict(sys.modules, _STUBS)
        cls._patcher.start()
        sys.modules.pop(_UPGRADE_STEPS_MOD, None)
        cls.mod = _load_script(_UPGRADE_STEPS_MOD, "upgrade_steps.py")

    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()
        sys.modules.pop(_UPGRADE_STEPS_MOD, None)

    def setUp(self):
        _STUBS["collective.big.bang.big"].setup_request.reset_mock()
        _STUBS["collective.big.bang.big"].setup_security.reset_mock()
        _STUBS["collective.big.bang.expansion"].upgrade_all_profiles.reset_mock()

    # ------------------------------------------------------------------
    # run_upgrade_steps() – happy path
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.upgrade_steps.noSecurityManager")
    @patch("collective.big.bang.scripts.upgrade_steps.upgrade_all_profiles")
    @patch("collective.big.bang.scripts.upgrade_steps.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.upgrade_steps.setup_request")
    def test_success(
        self,
        mock_setup_request,
        mock_setup_security,
        mock_upgrade,
        mock_no_sec,
    ):
        """Site present + security OK → upgrade runs, returns True."""
        app, container = _make_app_mock(object_ids=["Plone"])
        mock_setup_request.return_value = app

        with patch.dict(os.environ, {"SITE_ID": "Plone"}):
            result = self.mod.run_upgrade_steps(MagicMock())

        self.assertTrue(result)
        # upgrade_all_profiles called with portal_setup of the site object
        mock_upgrade.assert_called_once()
        mock_no_sec.assert_called()

    # ------------------------------------------------------------------
    # run_upgrade_steps() – site does not exist
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.upgrade_steps.noSecurityManager")
    @patch("collective.big.bang.scripts.upgrade_steps.upgrade_all_profiles")
    @patch("collective.big.bang.scripts.upgrade_steps.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.upgrade_steps.setup_request")
    def test_site_not_found(
        self, mock_setup_request, mock_setup_security, mock_upgrade, mock_no_sec
    ):
        """Site absent → returns False, upgrade never called."""
        app, _container = _make_app_mock(object_ids=[])
        mock_setup_request.return_value = app

        with patch.dict(os.environ, {"SITE_ID": "Plone"}):
            result = self.mod.run_upgrade_steps(MagicMock())

        self.assertFalse(result)
        mock_upgrade.assert_not_called()

    # ------------------------------------------------------------------
    # run_upgrade_steps() – setup_security fails
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.upgrade_steps.setup_security", return_value=False)
    @patch("collective.big.bang.scripts.upgrade_steps.setup_request")
    def test_security_fails(self, mock_setup_request, mock_setup_security):
        """setup_security=False → returns False immediately."""
        app, _ = _make_app_mock()
        mock_setup_request.return_value = app

        result = self.mod.run_upgrade_steps(MagicMock())

        self.assertFalse(result)

    # ------------------------------------------------------------------
    # run_upgrade_steps() – upgrade raises
    # ------------------------------------------------------------------

    @patch("collective.big.bang.scripts.upgrade_steps.noSecurityManager")
    @patch("collective.big.bang.scripts.upgrade_steps.upgrade_all_profiles")
    @patch("collective.big.bang.scripts.upgrade_steps.setup_security", return_value=True)
    @patch("collective.big.bang.scripts.upgrade_steps.setup_request")
    def test_upgrade_raises(
        self,
        mock_setup_request,
        mock_setup_security,
        mock_upgrade,
        mock_no_sec,
    ):
        """upgrade_all_profiles raises → logs error, returns False."""
        app, _container = _make_app_mock(object_ids=["Plone"])
        mock_setup_request.return_value = app
        mock_upgrade.side_effect = RuntimeError("upgrade failed")

        with patch.dict(os.environ, {"SITE_ID": "Plone"}):
            result = self.mod.run_upgrade_steps(MagicMock())

        self.assertFalse(result)
        mock_no_sec.assert_called()

    # ------------------------------------------------------------------
    # main()
    # ------------------------------------------------------------------

    def test_main_conf_not_found(self):
        """main() exits 1 when zope.conf path does not exist."""
        with patch("sys.argv", ["upgrade_steps", "/nonexistent/zope.conf"]):
            with patch("os.path.exists", return_value=False):
                with self.assertRaises(SystemExit) as cm:
                    self.mod.main()
        self.assertEqual(cm.exception.code, 1)

    def test_main_success(self):
        """main() exits 0 when run_upgrade_steps returns True."""
        zope2_mock, _ = _make_zope2_mock()
        with patch("sys.argv", ["upgrade_steps", "/path/to/zope.conf"]):
            with patch("os.path.exists", return_value=True):
                with patch.dict(sys.modules, {"Zope2": zope2_mock}):
                    with patch.object(self.mod, "run_upgrade_steps", return_value=True):
                        with self.assertRaises(SystemExit) as cm:
                            self.mod.main()
        self.assertEqual(cm.exception.code, 0)

    def test_main_failure(self):
        """main() exits 1 when run_upgrade_steps returns False."""
        zope2_mock, _ = _make_zope2_mock()
        with patch("sys.argv", ["upgrade_steps", "/path/to/zope.conf"]):
            with patch("os.path.exists", return_value=True):
                with patch.dict(sys.modules, {"Zope2": zope2_mock}):
                    with patch.object(self.mod, "run_upgrade_steps", return_value=False):
                        with self.assertRaises(SystemExit) as cm:
                            self.mod.main()
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
