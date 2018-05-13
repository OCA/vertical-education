
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError


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

    # TODO: ¿esto es necesario? como ahora se crean partners, yo creo que no
    # @api.multi
    # def create_student(self):
    #     self.ensure_one()
    #     ctx = self.env.context.copy()
    #     if 'default_type' in ctx:
    #         ctx.pop('default_type')
    #     student_obj = self.env['res.partner']
    #     ctx = self.env.context.copy()
    #     if 'default_type' in ctx:
    #         ctx.pop('default_type')
    #     values = {
    #         'name': self.partner_name,
    #         'user_id': self.user_id.id,
    #         'title': self.title.id,
    #         'street': self.street,
    #         'street2': self.street2,
    #         'city': self.city,
    #         'state_id': self.state_id.id,
    #         'country_id': self.country_id.id,
    #         'email': self.email_from,
    #         'phone': self.phone,
    #         'mobile': self.mobile,
    #         'zip': self.zip,
    #         'function': self.function
    #     }
    #     if not self.student_id:
    #         self.student_id = student_obj.with_context(ctx).create(values)
    #     else:
    #         raise ValidationError(
    #             _("the user already exist"))

    # TODO: check firstname lastname
    # def _onchange_partner_id_values(self, partner_id):
    #     values = super(Lead, self)._onchange_partner_id_values(partner_id)
    #     if partner_id:
    #         values.update({
    #             'contact_name': False,
    #             #'partner_name': self.partner_id.firstname,
    #             #'lastname': self.partner_id.lastname,
    #         })
    #     else:
    #         values = {
    #             'partner_name': False,
    #             'contact_name': False,
    #             #'lastname': False,
    #             'title': False,
    #             'street': False,
    #             'street2': False,
    #             'city': False,
    #             'state_id': False,
    #             'country_id': False,
    #             'email_from': False,
    #             'phone': False,
    #             'mobile': False,
    #             'zip': False,
    #             'function': False,
    #             'website': False,
    #         }
    #         return values
    #     return values

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
