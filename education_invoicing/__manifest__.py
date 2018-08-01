
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


{
    'name': 'Education Invoicing',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Sales',
    'sequence': 1,
    'complexity': 'easy',
    'author': 'PESOL, Odoo Community Association (OCA)',
    'depends': [
        'education',
        'account',
    ],
    'data': [
        'views/education_invoicing_method_view.xml',
        'views/education_enrollment_view.xml',
        'views/education_group_view.xml',
        'views/education_course_view.xml',
        'views/account_invoice_view.xml',
        'security/education_invoicing_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
