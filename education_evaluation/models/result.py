# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _


class EducationResult(models.Model):
    _name = 'education.result'

    exam_id = fields.Many2one(
        comodel_name='education.exam',
        string='Exam')

    score = fields.Float(
        string='Score')

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student')
