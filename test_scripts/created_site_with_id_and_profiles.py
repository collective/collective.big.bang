def main(app):
    if 'testingsite' not in app.objectIds():
        raise ValueError('Site not installed')

    site = app.get('testingsite')

    if site.language != 'fr':
        raise ValueError('Wrong site language : ' + site.language)

    installed_products = [product[0].split("-")[3].replace("_", ":")
                          for product in site.portal_setup.items()]

    if 'plone.app.caching:default' not in installed_products:
        raise ValueError('plone.app.caching was not installed')

    for package in ('plonetheme.barceloneta:default',
                    "plonetheme.classic:default",
                    "plonetheme.sunburst:default"):
        if package in installed_products:
            raise ValueError(package + ' is installed')

main(app)
