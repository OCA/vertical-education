# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EducationCrmTags(models.Model):
    _name = 'education.crm.tags'

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


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

    tag_pos_ids = fields.Many2many(
        comodel_name='education.crm.tags',
        string='Tags')

    stage = fields.Boolean(
        string='stage')

    date = fields.Date(
        string='Date')

    @api.model
    def create(self, vals):
        partner_id = self.env['res.partner'].browse(vals.get('partner_id'))
        if vals.get('course_id'):
            course_id = self.env['education.course'].browse(
                vals.get('course_id'))
            vals.update({
                'name': '%s' % (
                    course_id.name)
            })
        return super(Lead, self).create(vals)

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

    def _onchange_partner_id_values(self):
        partner = self.partner_id
        if partner:
            return {
                'partner_name': partner.firstname,
                'lastname': partner.lastname,
                'title': partner.title.id,
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id.id,
                'country_id': partner.country_id.id,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'zip': partner.zip,
                'function': partner.function,
            }
        else:
            return {}

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.update(self._onchange_partner_id_values())

    def create_enrollment(self):
        return {
            'name': 'Enrollment Registration',
            'type': 'ir.actions.act_window',
            'res_model': 'education.enrollment',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'form_view_id': 'education.education_enrollment_action',
            'context': {'default_lead_id': self.id}
        }
