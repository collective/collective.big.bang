def main(app):
    if 'Plone' not in app.objectIds():
        raise ValueError('Site not installed')

    site = app.get('Plone')

    if site.language != 'en':
        raise ValueError('Wrong site language : ' + site.language)
    installed_products = [product['id']
                          for product in site.portal_quickinstaller.listInstalledProducts()
                          if product['status'] == 'installed']
    if 'plonetheme.barceloneta' not in installed_products:
        raise ValueError('plonetheme.barceloneta not installed')
    if 'plone.app.caching' not in installed_products:
        raise ValueError('plone.app.caching not installed')

main(app)
