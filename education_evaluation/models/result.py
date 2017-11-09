# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class EducationResult(models.Model):
    _name = 'education.result'
    _inherit = ['mail.thread']

    exam_id = fields.Many2one(
        comodel_name='education.exam',
        string='Exam')

    score = fields.Float(
        string='Score')

    record_subject_id = fields.Many2one(
        comodel_name='education.record.subject',
        string='Subject Record')

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student',
        related='record_subject_id.record_id.student_id')


class EducationRecordSubject(models.Model):
    _inherit = 'education.record.subject'

    evaluation_result_ids = fields.One2many(
        comodel_name='education.result',
        inverse_name='record_subject_id',
        string='Evaluations')
