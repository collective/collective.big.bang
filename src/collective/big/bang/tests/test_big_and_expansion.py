# -*- coding: utf-8 -*-
"""Unit tests for big.py, expansion.py, event.py, interfaces.py, setuphandlers.py.

Follows the same stub/load pattern as test_scripts.py: inject stub modules into
sys.modules via ``patch.dict``, then load the real module under test from its
file path so all imports are satisfied without a running Zope/Plone instance.
"""
import importlib.util
import os
import sys
import unittest
from types import ModuleType
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

_PKG_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def _load_module(module_name, filename):
    """Load a package module directly from its file path, bypassing package discovery."""
    file_path = os.path.join(_PKG_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _mod(name):
    m = ModuleType(name)
    m.__spec__ = None
    return m


# ---------------------------------------------------------------------------
# Stub factory
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
        "plone.base",
        "plone.base.interfaces",
    ]:
        s[name] = _mod(name)

    s["plone"].api = s["plone.api"]
    s["plone.api"].env = s["plone.api.env"]
    s["plone.api.env"].plone_version = MagicMock(return_value="5.2.3")
    s["plone"].distribution = s["plone.distribution"]
    s["plone.distribution"].api = s["plone.distribution.api"]
    s["plone.distribution.api"].site = s["plone.distribution.api.site"]
    s["plone.distribution.api.site"]._create_site = MagicMock()
    s["plone"].base = s["plone.base"]
    s["plone.base"].interfaces = s["plone.base.interfaces"]
    s["plone.base.interfaces"].INonInstallable = MagicMock()

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
    s["Products.Five.browser"].BrowserView = object
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
    s["Zope2"].app = MagicMock()

    # ---- collective namespace ----
    s["collective"] = _mod("collective")
    s["collective"].__path__ = []
    s["collective"].__package__ = "collective"

    s["collective.big"] = _mod("collective.big")
    s["collective.big"].__path__ = []
    s["collective.big"].__package__ = "collective.big"
    s["collective"].big = s["collective.big"]

    cbg = _mod("collective.big.bang")
    cbg.__path__ = []
    cbg.__package__ = "collective.big.bang"
    s["collective.big"].bang = cbg
    s["collective.big.bang"] = cbg

    # interfaces stub (event.py imports IDarwinStartedEvent from here)
    cbg_ifaces = _mod("collective.big.bang.interfaces")
    cbg_ifaces.IDarwinStartedEvent = MagicMock()
    cbg.interfaces = cbg_ifaces
    s["collective.big.bang.interfaces"] = cbg_ifaces

    # event stub (big.py imports DarwinStartedEvent from here)
    cbg_event = _mod("collective.big.bang.event")
    cbg_event.DarwinStartedEvent = MagicMock()
    cbg.event = cbg_event
    s["collective.big.bang.event"] = cbg_event

    cbg_scripts = _mod("collective.big.bang.scripts")
    cbg_scripts.__path__ = []
    cbg_scripts.__package__ = "collective.big.bang.scripts"
    cbg.scripts = cbg_scripts
    s["collective.big.bang.scripts"] = cbg_scripts

    return s


_STUBS = _build_stubs()

# Module names used throughout
_BIG_MOD_NAME = "collective.big.bang.big"
_EXPANSION_MOD_NAME = "collective.big.bang.expansion"
_EVENT_MOD_NAME = "collective.big.bang.event"
_INTERFACES_MOD_NAME = "collective.big.bang.interfaces"
_SETUPHANDLERS_MOD_NAME = "collective.big.bang.setuphandlers"


# ===========================================================================
# Tests for big.py
# ===========================================================================

class TestBigPy(unittest.TestCase):
    """Tests for all functions in collective.big.bang.big."""

    @classmethod
    def setUpClass(cls):
        cls._patcher = patch.dict(sys.modules, _STUBS)
        cls._patcher.start()
        sys.modules.pop(_BIG_MOD_NAME, None)
        cls.mod = _load_module(_BIG_MOD_NAME, "big.py")

    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()
        sys.modules.pop(_BIG_MOD_NAME, None)

    def setUp(self):
        _STUBS["transaction"].commit.reset_mock()
        _STUBS["zope.component.hooks"].setSite.reset_mock()
        _STUBS["zope.event"].notify.reset_mock()
        _STUBS["zope.globalrequest"].setRequest.reset_mock()
        _STUBS["AccessControl.SecurityManagement"].newSecurityManager.reset_mock()
        _STUBS["AccessControl.SecurityManagement"].noSecurityManager.reset_mock()
        _STUBS["Testing.makerequest"].makerequest.reset_mock()
        _STUBS["Testing.makerequest"].makerequest.side_effect = lambda app: app
        _STUBS["Products.CMFPlone.factory"].addPloneSite.reset_mock()
        _STUBS["Zope2"].app.reset_mock()
        _STUBS["plone.api.env"].plone_version.reset_mock()
        _STUBS["plone.api.env"].plone_version.return_value = "5.2.3"

    # ------------------------------------------------------------------
    # get_bool_env
    # ------------------------------------------------------------------

    def test_get_bool_true_values(self):
        for val in ("true", "1", "yes"):
            with patch.dict(os.environ, {"_TEST_BB_VAR": val}):
                self.assertTrue(self.mod.get_bool_env("_TEST_BB_VAR", False))

    def test_get_bool_false_values(self):
        for val in ("false", "0", "no", ""):
            with patch.dict(os.environ, {"_TEST_BB_VAR": val}):
                self.assertFalse(self.mod.get_bool_env("_TEST_BB_VAR", True))

    def test_get_bool_env_default_false(self):
        os.environ.pop("_TEST_BB_NONEXISTENT", None)
        self.assertFalse(self.mod.get_bool_env("_TEST_BB_NONEXISTENT", False))

    def test_get_bool_env_default_true(self):
        os.environ.pop("_TEST_BB_NONEXISTENT", None)
        self.assertTrue(self.mod.get_bool_env("_TEST_BB_NONEXISTENT", True))

    # ------------------------------------------------------------------
    # setup_security
    # ------------------------------------------------------------------

    def test_setup_security_admin_found(self):
        app = MagicMock()
        user = MagicMock()
        user.__of__ = MagicMock(return_value=user)
        app.acl_users.getUser.return_value = user
        result = self.mod.setup_security(app)
        self.assertTrue(result)
        _STUBS["AccessControl.SecurityManagement"].newSecurityManager.assert_called_once()

    def test_setup_security_admin_not_found(self):
        app = MagicMock()
        app.acl_users.getUser.return_value = None
        result = self.mod.setup_security(app)
        self.assertFalse(result)
        _STUBS["AccessControl.SecurityManagement"].newSecurityManager.assert_not_called()

    # ------------------------------------------------------------------
    # setup_request
    # ------------------------------------------------------------------

    def test_setup_request_calls_makerequest_and_setrequest(self):
        app = MagicMock()
        _STUBS["Testing.makerequest"].makerequest.side_effect = lambda a: a
        result = self.mod.setup_request(app)
        _STUBS["Testing.makerequest"].makerequest.assert_called_once_with(app)
        _STUBS["zope.globalrequest"].setRequest.assert_called_once()
        self.assertIs(result, app)

    def test_setup_request_sets_parents(self):
        app = MagicMock()
        _STUBS["Testing.makerequest"].makerequest.side_effect = lambda a: a
        self.mod.setup_request(app)
        app.REQUEST.__setitem__.assert_called_once_with("PARENTS", [app])

    # ------------------------------------------------------------------
    # delete_site
    # ------------------------------------------------------------------

    def test_delete_site_exists(self):
        container = MagicMock()
        container.objectIds.return_value = ["Plone"]
        result = self.mod.delete_site(container, "Plone")
        self.assertTrue(result)
        container.manage_delObjects.assert_called_once_with(["Plone"])
        _STUBS["transaction"].commit.assert_called_once()

    def test_delete_site_absent(self):
        container = MagicMock()
        container.objectIds.return_value = []
        result = self.mod.delete_site(container, "Plone")
        self.assertFalse(result)
        container.manage_delObjects.assert_not_called()

    # ------------------------------------------------------------------
    # apply_additional_profiles
    # ------------------------------------------------------------------

    def test_apply_profiles_empty_string(self):
        site = MagicMock()
        self.mod.apply_additional_profiles(site, "")
        site.portal_setup.runAllImportStepsFromProfile.assert_not_called()

    def test_apply_profiles_adds_prefix(self):
        site = MagicMock()
        self.mod.apply_additional_profiles(site, "my.pkg:default")
        site.portal_setup.runAllImportStepsFromProfile.assert_called_once_with(
            "profile-my.pkg:default"
        )

    def test_apply_profiles_already_prefixed(self):
        site = MagicMock()
        self.mod.apply_additional_profiles(site, "profile-my.pkg:default")
        site.portal_setup.runAllImportStepsFromProfile.assert_called_once_with(
            "profile-my.pkg:default"
        )

    def test_apply_profiles_exception_logged(self):
        site = MagicMock()
        site.portal_setup.runAllImportStepsFromProfile.side_effect = Exception("fail")
        # Should not raise - logs error and continues
        self.mod.apply_additional_profiles(site, "my.pkg:default")

    def test_apply_profiles_multiple(self):
        site = MagicMock()
        self.mod.apply_additional_profiles(site, "a.pkg:default, b.pkg:default")
        self.assertEqual(
            site.portal_setup.runAllImportStepsFromProfile.call_count, 2
        )

    # ------------------------------------------------------------------
    # update_admin_password
    # ------------------------------------------------------------------

    def test_update_admin_password_set(self):
        app = MagicMock()
        app.acl_users.users = MagicMock()
        with patch.dict(os.environ, {"ADMIN_PASSWORD": "secret"}):
            self.mod.update_admin_password(app)
        app.acl_users.users.updateUserPassword.assert_called_once_with("admin", "secret")
        _STUBS["transaction"].commit.assert_called_once()

    def test_update_admin_password_not_set(self):
        app = MagicMock()
        os.environ.pop("ADMIN_PASSWORD", None)
        self.mod.update_admin_password(app)
        app.acl_users.users.updateUserPassword.assert_not_called()

    # ------------------------------------------------------------------
    # bang
    # ------------------------------------------------------------------

    def test_bang_inactive(self):
        with patch.dict(os.environ, {"ACTIVE_BIGBANG": "False"}):
            with patch.object(self.mod, "create_plone_site") as mock_create:
                self.mod.bang()
        mock_create.assert_not_called()
        _STUBS["Zope2"].app.assert_not_called()

    def test_bang_active_calls_create_and_update(self):
        app = MagicMock()
        site = MagicMock()
        app.unrestrictedTraverse.return_value = site
        _STUBS["Zope2"].app.return_value = app

        with patch.dict(os.environ, {"ACTIVE_BIGBANG": "True", "SITE_ID": "Plone"}):
            with patch.object(self.mod, "create_plone_site") as mock_create:
                with patch.object(self.mod, "update_admin_password") as mock_update:
                    self.mod.bang()

        mock_create.assert_called_once_with(app, "Plone")
        mock_update.assert_called_once_with(app)

    def test_bang_active_site_key_error_no_crash(self):
        app = MagicMock()
        app.unrestrictedTraverse.side_effect = KeyError("Plone")
        _STUBS["Zope2"].app.return_value = app

        with patch.dict(os.environ, {"ACTIVE_BIGBANG": "True", "SITE_ID": "Plone"}):
            with patch.object(self.mod, "create_plone_site"):
                with patch.object(self.mod, "update_admin_password"):
                    # Must not raise
                    self.mod.bang()

    # ------------------------------------------------------------------
    # create_plone_site
    # ------------------------------------------------------------------

    def test_create_plone_site_creates_new(self):
        app = MagicMock()
        container = MagicMock()
        container.objectIds.return_value = []
        app.unrestrictedTraverse.return_value = container

        with patch.object(self.mod, "setup_security", return_value=True):
            with patch.object(self.mod, "setup_request", return_value=app):
                self.mod.create_plone_site(app, "Plone")

        _STUBS["Products.CMFPlone.factory"].addPloneSite.assert_called_once()
        _STUBS["transaction"].commit.assert_called_once()

    def test_create_plone_site_already_exists(self):
        app = MagicMock()
        container = MagicMock()
        container.objectIds.return_value = ["Plone"]
        app.unrestrictedTraverse.return_value = container

        with patch.object(self.mod, "setup_request", return_value=app):
            self.mod.create_plone_site(app, "Plone")

        _STUBS["Products.CMFPlone.factory"].addPloneSite.assert_not_called()

    def test_create_plone_site_security_fails(self):
        app = MagicMock()
        container = MagicMock()
        container.objectIds.return_value = []
        app.unrestrictedTraverse.return_value = container

        with patch.object(self.mod, "setup_security", return_value=False):
            with patch.object(self.mod, "setup_request", return_value=app):
                self.mod.create_plone_site(app, "Plone")

        _STUBS["Products.CMFPlone.factory"].addPloneSite.assert_not_called()

    # ------------------------------------------------------------------
    # _default_packages_for_plone_version
    # ------------------------------------------------------------------

    def test_default_packages_plone_lt5(self):
        _STUBS["plone.api.env"].plone_version.return_value = "4.3.2"
        result = self.mod._default_packages_for_plone_version()
        self.assertIn("plonetheme.classic", result)
        self.assertIn("plonetheme.sunburst", result)

    def test_default_packages_plone_gte5(self):
        _STUBS["plone.api.env"].plone_version.return_value = "5.2.3"
        result = self.mod._default_packages_for_plone_version()
        self.assertIn("barceloneta", result)


# ===========================================================================
# Tests for expansion.py
# ===========================================================================

class TestExpansionPy(unittest.TestCase):
    """Tests for collective.big.bang.expansion."""

    @classmethod
    def setUpClass(cls):
        cls._patcher = patch.dict(sys.modules, _STUBS)
        cls._patcher.start()
        sys.modules.pop(_EXPANSION_MOD_NAME, None)
        cls.mod = _load_module(_EXPANSION_MOD_NAME, "expansion.py")

    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()
        sys.modules.pop(_EXPANSION_MOD_NAME, None)

    def setUp(self):
        _STUBS["transaction"].commit.reset_mock()
        _STUBS["zope.globalrequest"].setRequest.reset_mock()
        _STUBS["Testing.makerequest"].makerequest.reset_mock()
        _STUBS["Testing.makerequest"].makerequest.side_effect = lambda app: app
        _STUBS["Zope2"].app.reset_mock()
        _STUBS["Products.GenericSetup.upgrade"]._upgrade_registry.reset_mock()

    # ------------------------------------------------------------------
    # started
    # ------------------------------------------------------------------

    def test_started_inactive(self):
        with patch.dict(os.environ, {"ACTIVE_BIGBANG_EXPANSION": "False"}):
            with patch.object(self.mod, "upgrade_all_profiles") as mock_upgrade:
                self.mod.started(MagicMock())
        mock_upgrade.assert_not_called()

    def test_started_active_site_found(self):
        app = MagicMock()
        container = MagicMock()
        container.objectIds.return_value = ["Plone"]
        app.unrestrictedTraverse.return_value = container
        _STUBS["Zope2"].app.return_value = app

        with patch.dict(os.environ, {"ACTIVE_BIGBANG_EXPANSION": "True", "SITE_ID": "Plone"}):
            with patch.object(self.mod, "upgrade_all_profiles") as mock_upgrade:
                self.mod.started(MagicMock())

        mock_upgrade.assert_called_once()

    def test_started_active_site_absent(self):
        app = MagicMock()
        container = MagicMock()
        container.objectIds.return_value = []
        app.unrestrictedTraverse.return_value = container
        _STUBS["Zope2"].app.return_value = app

        with patch.dict(os.environ, {"ACTIVE_BIGBANG_EXPANSION": "True", "SITE_ID": "Plone"}):
            with patch.object(self.mod, "upgrade_all_profiles") as mock_upgrade:
                self.mod.started(MagicMock())

        mock_upgrade.assert_not_called()

    # ------------------------------------------------------------------
    # upgrade_all_profiles
    # ------------------------------------------------------------------

    def test_upgrade_all_profiles_no_pending(self):
        setup = MagicMock()
        setup.listProfilesWithPendingUpgrades.return_value = []
        with patch.object(self.mod, "upgrade_one_profile") as mock_one:
            self.mod.upgrade_all_profiles(setup)
        mock_one.assert_not_called()

    def test_upgrade_all_profiles_one_profile(self):
        setup = MagicMock()
        setup.listProfilesWithPendingUpgrades.return_value = ["my.package:default"]
        with patch.object(self.mod, "upgrade_one_profile") as mock_one:
            self.mod.upgrade_all_profiles(setup)
        mock_one.assert_called_once_with(setup, "my.package:default")

    def test_upgrade_all_profiles_multiple(self):
        setup = MagicMock()
        setup.listProfilesWithPendingUpgrades.return_value = ["a:default", "b:default"]
        with patch.object(self.mod, "upgrade_one_profile") as mock_one:
            self.mod.upgrade_all_profiles(setup)
        self.assertEqual(mock_one.call_count, 2)

    # ------------------------------------------------------------------
    # upgrade_one_profile
    # ------------------------------------------------------------------

    def test_upgrade_one_profile_no_upgrades(self):
        setup = MagicMock()
        with patch.object(self.mod, "list_upgrades", return_value=[]):
            with patch.object(self.mod, "do_upgrades") as mock_do:
                self.mod.upgrade_one_profile(setup, "my.pkg:default")
        mock_do.assert_not_called()

    def test_upgrade_one_profile_runs_until_done(self):
        setup = MagicMock()
        step = {"id": "s1", "dest": "2"}
        call_count = [0]

        def _list_upgrades_se(s, p):
            call_count[0] += 1
            return [step] if call_count[0] == 1 else []

        with patch.object(self.mod, "list_upgrades", side_effect=_list_upgrades_se):
            with patch.object(self.mod, "do_upgrades") as mock_do:
                self.mod.upgrade_one_profile(setup, "my.pkg:default")

        mock_do.assert_called_once_with(setup, "my.pkg:default", [step])

    # ------------------------------------------------------------------
    # list_upgrades
    # ------------------------------------------------------------------

    def test_list_upgrades_empty(self):
        setup = MagicMock()
        with patch.object(self.mod, "flatten_upgrades", return_value=iter([])):
            result = self.mod.list_upgrades(setup, "my.pkg:default")
        self.assertEqual(result, [])

    def test_list_upgrades_groups_by_dest(self):
        upgrades = [
            {"id": "s1", "dest": "2"},
            {"id": "s2", "dest": "2"},
            {"id": "s3", "dest": "3"},  # different dest – excluded
        ]
        setup = MagicMock()
        with patch.object(self.mod, "flatten_upgrades", return_value=iter(upgrades)):
            result = self.mod.list_upgrades(setup, "my.pkg:default")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "s1")
        self.assertEqual(result[1]["id"], "s2")

    # ------------------------------------------------------------------
    # flatten_upgrades
    # ------------------------------------------------------------------

    def test_flatten_upgrades_flat_list(self):
        setup = MagicMock()
        setup.listUpgrades.return_value = [{"id": "s1"}, {"id": "s2"}]
        result = list(self.mod.flatten_upgrades(setup, "my.pkg:default"))
        self.assertEqual(result, [{"id": "s1"}, {"id": "s2"}])

    def test_flatten_upgrades_nested_list(self):
        setup = MagicMock()
        setup.listUpgrades.return_value = [
            [{"id": "s1"}, {"id": "s2"}],
            {"id": "s3"},
        ]
        result = list(self.mod.flatten_upgrades(setup, "my.pkg:default"))
        self.assertEqual(result, [{"id": "s1"}, {"id": "s2"}, {"id": "s3"}])

    # ------------------------------------------------------------------
    # do_upgrades
    # ------------------------------------------------------------------

    def test_do_upgrades_runs_steps(self):
        setup = MagicMock()
        profile_id = "my.pkg:default"
        steps = [{"id": "s1", "ssource": "1", "sdest": "2", "title": "T", "dest": "2"}]

        step_mock = MagicMock()
        step_mock.checker = None
        step_mock.dest = ("2",)

        _STUBS["Products.GenericSetup.upgrade"]._upgrade_registry.getUpgradeStep.return_value = (
            step_mock
        )

        self.mod.do_upgrades(setup, profile_id, steps)

        step_mock.doStep.assert_called_once_with(setup)
        setup.setLastVersionForProfile.assert_called_once_with(profile_id, step_mock.dest)
        _STUBS["transaction"].commit.assert_called_once()

    def test_do_upgrades_raises_when_checker_set(self):
        setup = MagicMock()
        profile_id = "my.pkg:default"
        steps = [{"id": "s1", "ssource": "1", "sdest": "2", "title": "T", "dest": "2"}]

        step_mock = MagicMock()
        step_mock.checker = MagicMock()  # not None → raises ValueError
        step_mock.dest = ("2",)

        _STUBS["Products.GenericSetup.upgrade"]._upgrade_registry.getUpgradeStep.return_value = (
            step_mock
        )

        with self.assertRaises(ValueError):
            self.mod.do_upgrades(setup, profile_id, steps)


# ===========================================================================
# Tests for event.py
# ===========================================================================

class TestEventPy(unittest.TestCase):
    """Tests for collective.big.bang.event."""

    @classmethod
    def setUpClass(cls):
        # Need ObjectModifiedEvent to accept extra __init__ args
        class _OMEStub:
            def __init__(self, *args, **kwargs):
                pass

        stubs = dict(_STUBS)
        stubs["zope.lifecycleevent"].ObjectModifiedEvent = _OMEStub

        cls._patcher = patch.dict(sys.modules, stubs)
        cls._patcher.start()
        sys.modules.pop(_EVENT_MOD_NAME, None)
        cls.mod = _load_module(_EVENT_MOD_NAME, "event.py")

    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()
        sys.modules.pop(_EVENT_MOD_NAME, None)

    def test_darwin_started_event_instantiation(self):
        obj = MagicMock()
        event = self.mod.DarwinStartedEvent(obj)
        self.assertIsInstance(event, self.mod.DarwinStartedEvent)

    def test_darwin_started_event_is_a_class(self):
        self.assertTrue(isinstance(self.mod.DarwinStartedEvent, type))


# ===========================================================================
# Tests for interfaces.py
# ===========================================================================

class TestInterfacesPy(unittest.TestCase):
    """Tests for collective.big.bang.interfaces."""

    @classmethod
    def setUpClass(cls):
        cls._patcher = patch.dict(sys.modules, _STUBS)
        cls._patcher.start()
        sys.modules.pop(_INTERFACES_MOD_NAME, None)
        cls.mod = _load_module(_INTERFACES_MOD_NAME, "interfaces.py")

    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()
        sys.modules.pop(_INTERFACES_MOD_NAME, None)

    def test_idarwin_started_event_exists(self):
        self.assertTrue(hasattr(self.mod, "IDarwinStartedEvent"))

    def test_idarwin_started_event_is_accessible(self):
        self.assertIsNotNone(self.mod.IDarwinStartedEvent)


# ===========================================================================
# Tests for setuphandlers.py
# ===========================================================================

class TestSetuphandlersPy(unittest.TestCase):
    """Tests for collective.big.bang.setuphandlers."""

    @classmethod
    def setUpClass(cls):
        cls._patcher = patch.dict(sys.modules, _STUBS)
        cls._patcher.start()
        sys.modules.pop(_SETUPHANDLERS_MOD_NAME, None)
        cls.mod = _load_module(_SETUPHANDLERS_MOD_NAME, "setuphandlers.py")

    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()
        sys.modules.pop(_SETUPHANDLERS_MOD_NAME, None)

    def test_hidden_profiles_class_exists(self):
        self.assertTrue(hasattr(self.mod, "HiddenProfiles"))

    def test_get_non_installable_profiles_returns_list(self):
        obj = self.mod.HiddenProfiles()
        profiles = obj.getNonInstallableProfiles()
        self.assertIsInstance(profiles, list)

    def test_get_non_installable_profiles_contains_uninstall(self):
        obj = self.mod.HiddenProfiles()
        profiles = obj.getNonInstallableProfiles()
        self.assertIn("collective.big.bang:uninstall", profiles)


if __name__ == "__main__":
    unittest.main()
