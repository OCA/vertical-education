import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-vertical-education",
    description="Meta package for oca-vertical-education Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-openeducat_achievement',
        'odoo9-addon-openeducat_activity',
        'odoo9-addon-openeducat_admission',
        'odoo9-addon-openeducat_alumni',
        'odoo9-addon-openeducat_assignment',
        'odoo9-addon-openeducat_attendance',
        'odoo9-addon-openeducat_classroom',
        'odoo9-addon-openeducat_core',
        'odoo9-addon-openeducat_erp',
        'odoo9-addon-openeducat_exam',
        'odoo9-addon-openeducat_facility',
        'odoo9-addon-openeducat_fees',
        'odoo9-addon-openeducat_health',
        'odoo9-addon-openeducat_hostel',
        'odoo9-addon-openeducat_l10n_in',
        'odoo9-addon-openeducat_l10n_in_admission',
        'odoo9-addon-openeducat_library',
        'odoo9-addon-openeducat_parent',
        'odoo9-addon-openeducat_placement',
        'odoo9-addon-openeducat_scholarship',
        'odoo9-addon-openeducat_timetable',
        'odoo9-addon-openeducat_transportation',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 9.0',
    ]
)
