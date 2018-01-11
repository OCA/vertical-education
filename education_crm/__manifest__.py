# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


{
    'name': 'Education CRM',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'CRM',
    'sequence': 1,
    'complexity': 'easy',
    'author': 'PESOL, Odoo Community Association (OCA)',
    'depends': [
        'education',
        'crm',
    ],
    'data': [
        'views/education_crm_view.xml',
    ],
    'installable': True,
}
