# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EducationEnrollment(models.Model):
    _name = "education.enrollment"
    _rec_name = 'code'

    code = fields.Char(
        string='Code', required=True, default=lambda self: _('New'))
    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student', required=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course', required=True)
    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group', required=True)
    record_id = fields.Many2one(
        comodel_name='education.record',
        string='Record')
    subject_ids = fields.Many2many(
        comodel_name='education.subject',
        relation='enrollment_subject_rel',
        string='Subjects')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('done', 'Done'),
         ('cancel', 'Cancelled')],
        string='Status',
        default="draft")

    @api.multi
    def action_draft(self):
        self.ensure_one()
        self.state = 'draft'

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancel'

    @api.multi
    def action_done(self):
        self.ensure_one()
        record_obj = self.env['education.record']
        record = record_obj.search([
            ('student_id', '=', self.student_id.id),
            ('course_id', '=', self.course_id.id)
        ], limit=1)

        if not record:
            record_subject_values = [
                (0, 0, {'subject_id': subject.id})
                for subject in self.subject_ids
            ]
            record = record_obj.create({
                'student_id': self.student_id.id,
                'course_id': self.course_id.id,
                'record_subject_ids': record_subject_values
            })
        self.write({
            'state': 'done',
            'record_id': record.id
        })

    @api.onchange('course_id')
    def onchange_course_id(self):
        if self.course_id:
            self.subject_ids = [(6, 0, self.course_id.subject_ids.ids)]
        else:
            self.subject_ids = False
        self.group_id = False

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.enrollment') or 'New'
        return super(EducationEnrollment, self).create(vals)
