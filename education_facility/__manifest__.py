# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    'name': 'Education Facility',
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Facility',
    'complexity': "easy",
    'author': 'Tech Receptives, PESOL, Odoo Community Association (OCA)',
    'depends': ['education'],
    'data': [
        'views/facility_view.xml',
        'views/facility_line_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/facility_demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
