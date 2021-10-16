import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-vertical-education",
    description="Meta package for oca-vertical-education Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-openeducat_erp',
        'odoo10-addon-openeducat_fees',
        'odoo10-addon-openeducat_support',
        'odoo10-addon-web_openeducat',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 10.0',
    ]
)
