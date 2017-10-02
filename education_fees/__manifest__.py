# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    'name': 'Education Fees',
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Fees',
    'complexity': "easy",
    'author': 'Tech Receptives, PESOL, Odoo Community Association (OCA)',
    'depends': ['education', 'account_accountant'],
    'data': [
        'views/fees_terms_view.xml',
        'views/course_view.xml',
        'security/fees_security.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/fees_terms_line_demo.xml',
        'demo/fees_terms_demo.xml',
        'demo/course_demo.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
