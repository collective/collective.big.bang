from Products.Five.browser import BrowserView
from Products.GenericSetup.upgrade import _upgrade_registry
from Testing.makerequest import makerequest
from zope.globalrequest import setRequest

# from zope.interface import Interface
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import os
import logging
import transaction
import Zope2

logger = logging.getLogger("collective.big.bang.expansion")

# class IMyView(Interface):
#     """Marker Interface for IMyView"""


def started(event):
    is_expansion_active = os.getenv("ACTIVE_BIGBANG_EXPANSION", False)
    if is_expansion_active == "True":
        app = Zope2.app()
        app = makerequest(app)
        app.REQUEST["PARENTS"] = [app]
        setRequest(app.REQUEST)
        container = app.unrestrictedTraverse("/")

        site_id = os.getenv("SITE_ID", "Plone")
        oids = container.objectIds()
        if site_id in oids and "/" not in site_id:
            site = getattr(app, site_id, None)
            portal_setup = site.portal_setup
            upgrade_all_profiles(portal_setup)


class ExpansionView(BrowserView):
    # If you want to define a template here, please remove the template attribute from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('my_view.pt')

    def __call__(self):
        # your code here

        # render the template
        return self.index()


def upgrade_all_profiles(portal_setup):
    """Upgrade the profiles."""
    upgrade_profiles = portal_setup.listProfilesWithPendingUpgrades()
    for upgrade_profile in upgrade_profiles:
        upgrade_one_profile(portal_setup, upgrade_profile)


def upgrade_one_profile(setup, profile_id):
    upgrades = list_upgrades(setup, profile_id)
    if not upgrades:
        logger.info("Nothing to upgrade for profile {0}".format(profile_id))
        return
    while upgrades:
        do_upgrades(setup, profile_id, upgrades)
        upgrades = list_upgrades(setup, profile_id)
    else:
        logger.info("Finished upgrading {0} profile".format(profile_id))


def list_upgrades(setup, profile_id):
    """Return only the upgrade steps needed to get to the next version."""
    all_upgrades = list(flatten_upgrades(setup, profile_id))
    if not all_upgrades:
        return all_upgrades
    dest = all_upgrades[0]["dest"]
    upgrades = []
    for info in all_upgrades:
        if info["dest"] != dest:
            break
        upgrades.append(info)
    return upgrades


def flatten_upgrades(setup, profile_id):
    for info in setup.listUpgrades(profile_id):
        if isinstance(info, list):
            for subinfo in info:
                yield subinfo
        else:
            yield info


def do_upgrades(setup, profile_id, steps_to_run):
    """Perform all selected upgrade steps."""
    step = None
    if steps_to_run:
        logger.info(
            "Upgrading profile {0} to {1}".format(profile_id, steps_to_run[0]["sdest"])
        )
    for info in steps_to_run:
        step = _upgrade_registry.getUpgradeStep(profile_id, info["id"])
        if step is not None:
            msg = "profile {0} from {ssource} to {sdest}: {title}".format(
                profile_id, **info
            )
            logger.info("Running upgrade step for {0}.".format(msg))
            step.doStep(setup)
            logger.info("Finished upgrade step for {0}.".format(msg))

    # We update the profile version to the last one we have reached
    # with running an upgrade step.
    if step and step.dest is not None and step.checker is None:
        setup.setLastVersionForProfile(profile_id, step.dest)
    else:
        raise ValueError(
            "Upgrade steps {0} finished for profile {1} "
            "but no new version {2} recorded.".format(
                steps_to_run, profile_id, ".".join(step.dest)
            )
        )

    transaction.commit()
