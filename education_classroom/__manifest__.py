# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    'name': 'Education Classroom',
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Classroom',
    'complexity': "easy",
    'author': 'Tech Receptives, PESOL, Odoo Community Association (OCA)',
    'depends': ['education', 'education_facility', 'product'],
    'data': [
        'views/classroom_view.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/classroom_demo.xml',
        'demo/facility_line_demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
