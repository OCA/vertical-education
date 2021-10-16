import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-vertical-education",
    description="Meta package for oca-vertical-education Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-openeducat_erp',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 8.0',
    ]
)
