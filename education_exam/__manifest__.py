# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    'name': 'Education Exam',
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Exam',
    'complexity': "easy",
    'author': 'Tech Receptives, PESOL, Odoo Community Association (OCA)',
    'depends': ['education', 'education_classroom'],
    'data': [
        'views/exam_attendees_view.xml',
        'views/exam_room_view.xml',
        'views/exam_session_view.xml',
        'views/exam_type_view.xml',
        'wizard/room_distribution_view.xml',
        'wizard/held_exam_view.xml',
        'views/exam_view.xml',
        'views/marksheet_line_view.xml',
        'views/marksheet_register_view.xml',
        'views/grade_configuration_view.xml',
        'views/result_line_view.xml',
        'views/result_template_view.xml',
        'report/report_ticket.xml',
        'report/student_marksheet.xml',
        #         'report/report_exam_student_label.xml',
        'report/report_menu.xml',
        'wizard/student_hall_tickets_wizard_view.xml',
        'security/ir.model.access.csv',
        'views/exam_menu.xml',
    ],
    'demo': [
        'demo/exam_room_demo.xml',
        'demo/exam_type_demo.xml',
        'demo/exam_session_demo.xml',
        'demo/exam_demo.xml',
        'demo/exam_attendees_demo.xml',
        'demo/grade_configuration_demo.xml',
        'demo/result_template_demo.xml',
        #         'demo/marksheet_register_demo.xml',
        #         'demo/marksheet_line_demo.xml',
        #         'demo/result_line_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
