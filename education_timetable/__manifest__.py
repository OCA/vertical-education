# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


{
    'name': 'Education Timetable',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Education',
    'sequence': 1,
    'complexity': 'easy',
    'author': 'PESOL, Odoo Community Association (OCA)',
    'depends': [
        'base',
        'education',
        'calendar',
        'mail'
    ],
    'data': [
        'views/timetable_line_view.xml',
        'views/session_view.xml',
        'views/timerange_view.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'wizard/session_presence_view.xml',
        'security/timetable_security.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/timerange_demo.xml',
        'demo/timetable_demo.xml',
    ],
    'installable': True,
}
