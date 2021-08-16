# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.big.bang


class CollectiveBigbangLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.big.bang)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.big.bang:default")


COLLECTIVE_BIG_BANG_FIXTURE = CollectiveBigbangLayer()


COLLECTIVE_BIG_BANG_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_BIG_BANG_FIXTURE,),
    name="CollectiveBigbangLayer:IntegrationTesting",
)


COLLECTIVE_BIG_BANG_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_BIG_BANG_FIXTURE,),
    name="CollectiveBigbangLayer:FunctionalTesting",
)


COLLECTIVE_BIG_BANG_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_BIG_BANG_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveBigbangLayer:AcceptanceTesting",
)
