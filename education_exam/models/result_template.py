# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpResultTemplate(models.Model):
    _name = 'education.result.template'
    _description = 'Result Template'
    _rec_name = 'name'

    exam_session_id = fields.Many2one(
        'education.exam.session', 'Exam Session', required=True)
    evolution_type = fields.Selection(
        related='exam_session_id.evolution_type', store=True)
    name = fields.Char("Name", size=254, required=True)
    result_date = fields.Date(
        'Result Date', required=True, default=fields.Date.today())
    grade_ids = fields.Many2many(
        'education.grade.configuration', string='Grade Configuration')
    state = fields.Selection(
        [('draft', 'Draft'), ('result_generated', 'Result Generated')],
        'State', default='draft')

    @api.multi
    @api.constrains('exam_session_id')
    def _check_exam_session(self):
        for record in self:
            for exam in record.exam_session_id.exam_ids:
                if exam.state != 'done':
                    raise ValidationError(
                        _('All subject exam should be done.'))

    @api.multi
    @api.constrains('grade_ids')
    def _check_min_max_per(self):
        for record in self:
            count = 0
            for grade in record.grade_ids:
                for sub_grade in record.grade_ids:
                    if grade != sub_grade:
                        if (sub_grade.min_per <= grade.min_per and
                                sub_grade.max_per >= grade.min_per) or \
                                (sub_grade.min_per <= grade.max_per and
                                 sub_grade.max_per >= grade.max_per):
                            count += 1
            if count > 0:
                raise ValidationError(
                    _('Percentage range conflict with other record.'))

    @api.multi
    def generate_result(self):
        for record in self:
            marksheet_reg_id = self.env['education.marksheet.register'].create({
                'name': 'Mark Sheet for %s' % record.exam_session_id.name,
                'exam_session_id': record.exam_session_id.id,
                'generated_date': fields.Date.today(),
                'generated_by': self.env.uid,
                'status': 'draft',
                'result_template_id': record.id
            })
            student_dict = {}
            for exam in record.exam_session_id.exam_ids:
                for attendee in exam.attendees_line:
                    result_line_id = self.env['education.result.line'].create({
                        'student_id': attendee.student_id.id,
                        'exam_id': exam.id,
                        'marks': str(attendee.marks and attendee.marks or 0),
                    })
                    if attendee.student_id.id not in student_dict:
                        student_dict[attendee.student_id.id] = []
                    student_dict[attendee.student_id.id].append(result_line_id)
            for student in student_dict:
                marksheet_line_id = self.env['education.marksheet.line'].create({
                    'student_id': student,
                    'marksheet_reg_id': marksheet_reg_id.id,
                })
                for result_line in student_dict[student]:
                    result_line.marksheet_line_id = marksheet_line_id
            record.state = 'result_generated'
