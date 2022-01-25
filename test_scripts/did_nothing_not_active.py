import os


def main(app):
    site_id = os.getenv("SITE_ID", "Plone")
    if site_id in app.objectIds():
        exit(1)


main(app)
