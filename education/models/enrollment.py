# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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
        [('pending', 'Pending'),
         ('active', 'Active'),
         ('cancelled', 'Cancelled'),
         ('drop', 'Drop'),
         ('finished', 'Finished')],
        string='Status',
        default="pending")

    @api.multi
    def do_toggle_submitted(self):
        self.state = 'active'

    @api.multi
    def do_toggle_approve(self):
        for record in self:
            subject_ids = []
            for sub in record.subject_ids:
                subject_ids.append(sub.id)
                course_id = self.env['education.record'].search([
                    ('student_id', '=', record.student_id.id),
                    ('course_id', '=', record.course_id.id)
                ], limit=1)
                if course_id:
                    course_id.write({
                        'subject_ids': [[6, 0, list(set(subject_ids))]]
                    })
                    record.state = 'finished'
                else:
                    raise ValidationError(
                        _("Course not found on student's records!"))

    @api.multi
    def action_reset_draft(self):
        self.state = 'pending'

    @api.multi
    def cancelled_enrollment(self):
        self.state = 'cancelled'

    @api.multi
    def get_subjects(self):
        for record in self:
            subject_ids = []
            if record.course_id and record.course_id.subject_ids:
                for subject in record.course_id.subject_ids:
                    subject_ids.append(subject.id)
            record.subject_ids = [(6, 0, subject_ids)]

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.enrollment') or 'New'
        return super(EducationEnrollment, self).create(vals)
