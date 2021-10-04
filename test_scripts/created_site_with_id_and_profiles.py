def main(app):
    if 'testingsite' not in app.objectIds():
        raise ValueError('Site not installed')

    site = app.get('testingsite')

    if site.language != 'fr':
        raise ValueError('Wrong site language : ' + site.language)
    installed_products = [product['id']
                          for product in site.portal_quickinstaller.listInstalledProducts()
                          if product['status'] == 'installed']
    if 'plonetheme.barceloneta' not in installed_products:
        raise ValueError('plonetheme.barceloneta not installed')
    if 'plone.app.caching' in installed_products:
        raise ValueError('plone.app.caching is installed')

main(app)
