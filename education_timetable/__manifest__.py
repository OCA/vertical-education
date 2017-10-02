# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    'name': 'Education Timetable',
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage TimeTables',
    'complexity': "easy",
    'author': 'Tech Receptives, PESOL, Odoo Community Association (OCA)',
    'depends': ['education_classroom'],
    'data': [
        'views/timetable_view.xml',
        'views/timing_view.xml',
        'views/faculty_view.xml',
        'report/report_timetable_student_generate.xml',
        'report/report_timetable_teacher_generate.xml',
        'report/report_menu.xml',
        'wizard/generate_timetable_view.xml',
        'wizard/time_table_report.xml',
        'dashboard/timetable_student_dashboard.xml',
        'dashboard/timetable_faculty_dashboard.xml',
        'security/ir.model.access.csv',
        'security/education_timetable_security.xml',
        'views/timetable_menu.xml',
        'wizard/session_confirmation.xml',
        'views/timetable_templates.xml',
    ],
    'demo': [
        'demo/timing_demo.xml',
        'demo/education_timetable_demo.xml'
    ],
    'test': [
        'test/timetable_sub_value.yml',
        'test/generate_timetable.yml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
