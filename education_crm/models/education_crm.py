# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Lead(models.Model):
    _inherit = 'crm.lead'

    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group')

    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course')

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student')

    enrollment_id = fields.Many2one(
        comodel_name='education.enrollment',
        string='Enrollment')

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        related="student_id.partner_id",
        store=True)

    @api.multi
    def create_student(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        if 'default_type' in ctx:
            ctx.pop('default_type')
        student_obj = self.env['education.student']
        ctx = self.env.context.copy()
        if 'default_type' in ctx:
            ctx.pop('default_type')
        values = {
            'name': self.partner_name,
            'user_id': self.user_id.id,
            'title': self.title.id,
            'street': self.street,
            'street2': self.street2,
            'city': self.city,
            'state_id': self.state_id.id,
            'country_id': self.country_id.id,
            'email': self.email_from,
            'phone': self.phone,
            'mobile': self.mobile,
            'zip': self.zip,
            'function': self.function
        }
        if not self.student_id:
            self.student_id = student_obj.with_context(ctx).create(values)
        else:
            raise ValidationError(
                _("the user already exist"))

    def _onchange_student_id_values(self):
        student = self.student_id
        if student:
            return {
                'partner_name': student.name,
                'title': student.title.id,
                'street': student.street,
                'street2': student.street2,
                'city': student.city,
                'state_id': student.state_id.id,
                'country_id': student.country_id.id,
                'email_from': student.email,
                'phone': student.phone,
                'mobile': student.mobile,
                'zip': student.zip,
                'function': student.function,
            }
        else:
            return {}

    @api.onchange('student_id')
    def _onchange_student_id(self):
        self.update(self._onchange_student_id_values())

    def create_enrollment(self):
        # TODO: el grupo no es obligatorio para crear la matricula
        # crear la matricula para asociarla al lead
        # y simplemente mostrar el lead creado, en lugar de mostrar el
        # formulario para crear
        return {
            'name': 'Enrollment Registration',
            'type': 'ir.actions.act_window',
            'res_model': 'education.enrollment',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'form_view_id': 'education.education_enrollment_action',
        }
