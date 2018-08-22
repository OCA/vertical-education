
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Education",
    "summary": "Education Management for Odoo",
    "version": "11.0.1.0.0",
    "category": "Education",
    "website": "https://github.com/OCA/vertical_education",
    "author": "PESOL, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "base",
        'mail'
    ],
    "data": [
        'views/menu_view.xml',
        'views/course_view.xml',
        'views/course_category_view.xml',
        'views/subject_view.xml',
        'views/enrollment_view.xml',
        'views/group_view.xml',
        'views/record_subject_group_view.xml',
        'views/record_view.xml',
        'views/record_subject_view.xml',
        'views/partner_view.xml',
        'security/education_security.xml',
        'security/ir.model.access.csv',
    ],
    "demo": [
        'demo/education_res_partner_demo.xml',
        'demo/education_subject_demo.xml',
        'demo/education_teacher_demo.xml',
        'demo/education_student_demo.xml',
        'demo/education_course_demo.xml',
        'demo/education_group_demo.xml',
        'demo/education_enrollment_demo.xml',
        'demo/education_grading_scale.xml'
    ],
}
