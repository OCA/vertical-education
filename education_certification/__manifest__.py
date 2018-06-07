# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


{
    'name': 'Education Certification',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Education',
    'sequence': 1,
    'complexity': 'easy',
    'author': 'PESOL, Odoo Community Association (OCA)',
    'depends': [
        'education',
    ],
    'data': [
        'views/certification_view.xml',
        'security/certification_security.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
}
