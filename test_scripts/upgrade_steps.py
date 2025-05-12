from collective.big.bang.big import create_plone_site
from collective.big.bang.expansion import upgrade_all_profiles

import os
import transaction


def main(app):
    site_id = os.getenv("SITE_ID", "Plone")
    if site_id in app.objectIds():
        del app[site_id]
    create_plone_site(app, site_id)
    assert site_id in app.objectIds(), "Plone site not existing"
    plone = app.get(site_id)

    setup = plone.portal_setup
    profile_id = "profile-plone.restapi:default"
    restapi_profile_upgrades = setup.listUpgrades(profile_id)
    second_to_last_profile_upgrade = sorted(
        restapi_profile_upgrades, key=lambda x: x["sdest"], reverse=True
    )[1]
    step = second_to_last_profile_upgrade.get("step")
    setup.setLastVersionForProfile(profile_id, step.dest)
    assert "plone.restapi:default" in setup.listProfilesWithPendingUpgrades()
    upgrade_all_profiles(setup)
    assert [] == setup.listProfilesWithPendingUpgrades()
    del app[site_id]
    transaction.commit()


main(app)  # noqa
