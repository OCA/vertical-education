# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EducationGroup(models.Model):
    _name = "education.group"
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char(
        string='Name', required=True)

    code = fields.Char(
        string='Code', required=True, default=lambda self: _('New'))
    course_id = fields.Many2one(
        comodel_name='education.course',
        required=True,
        string="Course")
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    enrollment_ids = fields.One2many(
        comodel_name='education.enrollment',
        inverse_name='group_id',
        string='Enrollments')
    tutor_id = fields.Many2one(
        comodel_name='education.teacher',
        string='Tutor')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('active', 'Active'),
         ('done', 'Done'),
         ('cancel', 'Cancelled')],
        string='Status',
        default="draft")

    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the Group without removing it.")


    def action_draft(self):
        self.ensure_one()
        self.state = 'draft'

    def action_active(self):
        self.ensure_one()
        self.state = 'active'

    def action_done(self):
        self.ensure_one()
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.group') or 'New'
        return super(EducationGroup, self).create(vals)

    @api.multi
    def unlink(self):
        if self.enrollment_ids:
            raise ValidationError(
                _('You can not delete a group with registered students'))
        else:
            super(EducationGroup, self).unlink()
