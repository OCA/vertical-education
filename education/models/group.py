# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EducationGroup(models.Model):
    _name = "education.group"
    _rec_name = 'code'

    name = fields.Char(
        string='Name', required=True)

    code = fields.Char(
        string='Code', required=True, default=lambda self: _('New'))

    course_id = fields.Many2one(
        comodel_name='education.course',
        required=True,
        string="Course")
    record_ids = fields.One2many(
        comodel_name='education.record',
        inverse_name='group_id',
        string='Records')

    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    enrollment_ids = fields.One2many(
        comodel_name='education.enrollment',
        inverse_name='group_id',
        string='Enrollments')

    teacher_in_charge = fields.Many2one(
        comodel_name='education.teacher',
        string='Teacher in charge')

    state = fields.Selection(
        [('pending', 'Pending'),
         ('active', 'Active'),
         ('cancelled', 'Cancelled'),
         ('done', 'Done')],
        string='Status',
        default="pending")

    @api.multi
    def do_toggle_active(self):
        self.state = 'active'

    @api.multi
    def do_toggle_cancelled(self):
        self.state = 'cancelled'
        if self.record_ids:
            for record in self.record_ids:
                for line in record.student_id.record_ids:
                    if record.code == line.code:
                        line.unlink()

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.group') or 'New'
        return super(EducationGroup, self).create(vals)
