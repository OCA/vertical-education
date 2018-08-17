# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields

class Lead(models.Model):
    _inherit = 'crm.lead'

    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group')

    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course')

    enrollment_id = fields.Many2one(
        comodel_name='education.enrollment',
        string='Enrollment')

    def create_enrollment(self):
        return {
            'name': 'Enrollment Registration',
            'type': 'ir.actions.act_window',
            'res_model': 'education.enrollment',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'form_view_id': 'education.education_enrollment_action',
            'context': {'default_lead_id': self.id,
                        'default_student_id': self.partner_id.id,
                        'default_course_id': self.course_id.id,
                        }
        }
