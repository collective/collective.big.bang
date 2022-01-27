import os


def main(app):
    site_id = os.getenv("SITE_ID", "Plone")
    if "/" not in site_id:
        print("wrong site_id : " + site_id)
        exit(1)
    if site_id in app.objectIds() or site_id.split("/")[0]:
        print("Site was created : " + site_id)
        exit(1)


main(app)
