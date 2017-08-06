# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.exceptions import ValidationError
from openerp import models, fields, api, _


class EducationSubjectRegistration(models.Model):
    _name = 'education.subject.registration'
    _inherit = ['mail.thread']

    name = fields.Char('Name', readonly=True, default='New')
    student_id = fields.Many2one('education.student', 'Student', required=True,
                                 track_visibility='onchange')
    course_id = fields.Many2one('education.course', 'Course', required=True,
                                track_visibility='onchange')
    batch_id = fields.Many2one('education.batch', 'Batch', required=True,
                               track_visibility='onchange')
    compulsory_subject_ids = fields.Many2many(
        'education.subject', 'subject_compulsory_rel',
        'register_id', 'subject_id', string="Compulsory Subjects",
        readonly=True)
    elective_subject_ids = fields.Many2many(
        'education.subject', string="Elective Subjects")
    state = fields.Selection([
        ('draft', 'Draft'), ('submitted', 'Submitted'),
        ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='draft', string='state', copy=False,
        track_visibility='onchange')
    max_unit_load = fields.Float('Maximum Unit Load',
                                 track_visibility='onchange')
    min_unit_load = fields.Float('Minimum Unit Load',
                                 track_visibility='onchange')

    @api.multi
    def action_reset_draft(self):
        self.state = 'draft'

    @api.multi
    def action_reject(self):
        self.state = 'rejected'

    @api.multi
    def action_approve(self):
        for record in self:
            subject_ids = []
            for sub in record.compulsory_subject_ids:
                subject_ids.append(sub.id)
            for sub in record.elective_subject_ids:
                subject_ids.append(sub.id)
            course_id = self.env['education.student.course'].search([
                ('student_id', '=', record.student_id.id),
                ('course_id', '=', record.course_id.id)
            ], limit=1)
            if course_id:
                course_id.write({
                    'subject_ids': [[6, 0, list(set(subject_ids))]]
                })
                record.state = 'approved'
            else:
                raise ValidationError(
                    _("Course not found on student's admission!"))

    @api.multi
    def action_submitted(self):
        self.state = 'submitted'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'education.subject.registration') or '/'
        return super(EducationSubjectRegistration, self).create(vals)

    @api.multi
    def get_subjects(self):
        for record in self:
            subject_ids = []
            if record.course_id and record.course_id.subject_ids:
                for subject in record.course_id.subject_ids:
                    if subject.subject_type == 'compulsory':
                        subject_ids.append(subject.id)
            record.compulsory_subject_ids = [(6, 0, subject_ids)]
