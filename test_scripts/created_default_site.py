from collective.big.bang.big import _default_packages_for_plone_version


def main(app):
    if 'Plone' not in app.objectIds():
        raise ValueError('Site not installed')

    site = app.get('Plone')
    if site.language != 'en':
        raise ValueError('Wrong site language : ' + site.language)

    installed_products = [product[0].split("-")[3].replace("_", ":")
                          for product in site.portal_setup.items()]
    to_check = [package.strip() for package in _default_packages_for_plone_version().split(',')]
    for package in to_check:
        if package not in installed_products:
            raise ValueError(package + ' not installed')


main(app)
