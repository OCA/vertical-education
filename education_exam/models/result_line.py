# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpResultLine(models.Model):
    _name = 'education.result.line'
    _rec_name = 'marks'

    marksheet_line_id = fields.Many2one(
        'education.marksheet.line', 'Marksheet Line', ondelete='cascade')
    exam_id = fields.Many2one('education.exam', 'Exam', required=True)
    evolution_type = fields.Selection(
        related='exam_id.session_id.evolution_type', store=True)
    marks = fields.Integer('Marks', required=True)
    grade = fields.Char('Grade', readonly=True, compute='_compute_grade')
    student_id = fields.Many2one('education.student', 'Student', required=True)
    status = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], 'Status',
                              compute='_compute_status')

    @api.constrains('marks', 'marks')
    def _check_marks(self):
        if (self.marks < 0.0):
            raise ValidationError(_("Enter proper Marks or Percentage!"))

    @api.multi
    @api.depends('marks')
    def _compute_grade(self):
        for record in self:
            if record.evolution_type == 'grade':
                grades = record.marksheet_line_id.marksheet_reg_id.\
                    result_template_id.grade_ids
                for grade in grades:
                    if grade.min_per <= record.marks and \
                            grade.max_per >= record.marks:
                        record.grade = grade.result

    @api.multi
    @api.depends('marks')
    def _compute_status(self):
        for record in self:
            record.status = 'pass'
            if record.marks < record.exam_id.min_marks:
                record.status = 'fail'
