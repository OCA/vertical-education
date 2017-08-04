# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    'name': 'Education',
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'sequence': 1,
    'summary': 'Manage Students, Faculties and Education Institute',
    'complexity': 'easy',
    'author': 'Tech Receptives, PESOL, Odoo Community Association (OCA)',
    'depends': [
        'board',
        'document',
        'hr',
        'partner_contact_gender',
        'partner_firstname',
        'partner_second_lastname',
        'partner_contact_birthdate',
        'partner_contact_nationality'
    ],
    'data': [
        'report/report_menu.xml',
        'report/report_student_bonafide.xml',
        'report/report_student_idcard.xml',
        'wizard/faculty_create_employee_wizard_view.xml',
        'security/education_security.xml',
        'security/ir.model.access.csv',
        'views/student_view.xml',
        'views/hr_view.xml',
        'views/course_view.xml',
        'views/batch_view.xml',
        'views/subject_view.xml',
        'views/faculty_view.xml',
        'views/res_company_view.xml',
        'views/subject_registration_view.xml',
        'dashboard/student_dashboard_view.xml',
        'dashboard/faculty_dashboard_view.xml',
        'menu/education_menu.xml',
        'menu/faculty_menu.xml',
        'menu/student_menu.xml',
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/subject_demo.xml',
        'demo/course_demo.xml',
        'demo/batch_demo.xml',
        'demo/student_demo.xml',
        'demo/student_course_demo.xml',
        'demo/faculty_demo.xml',
    ],
    'test': [
        'test/res_users_test.yml',
        'test/faculty_emp_user_creation.yml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
