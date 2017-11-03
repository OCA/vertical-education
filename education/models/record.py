# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EducationRecord(models.Model):
    _name = "education.record"

    code = fields.Char(
        string='Code', required=True, default=lambda self: _('New'))

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student', required=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course', required=True)
    enrollment_ids = fields.One2many(
        comodel_name='education.enrollment',
        inverse_name='record_id',
        string='Enrollments')
    record_subject_ids = fields.One2many(
        comodel_name='education.record.subject',
        inverse_name='record_id',
        string='Enrollments')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.record') or 'New'
        return super(EducationRecord, self).create(vals)


class EducationRecordSubject(models.Model):
    _name = "education.record.subject"
    _rec_name = 'subject_id'

    subject_id = fields.Many2one(
        comodel_name='education.subject',
        string='Subject')
    record_id = fields.Many2one(
        comodel_name='education.record',
        string='Record')
