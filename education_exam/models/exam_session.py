# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExamSession(models.Model):
    _name = 'education.exam.session'
    _description = 'Exam Session'

    name = fields.Char('Exam Session', size=256, required=True)
    course_id = fields.Many2one('education.course', 'Course', required=True)
    batch_id = fields.Many2one('education.batch', 'Batch', required=True)
    exam_code = fields.Char('Exam Session Code', size=8, required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    exam_ids = fields.One2many('education.exam', 'session_id', 'Exam(s)')
    exam_type = fields.Many2one(
        'education.exam.type', 'Exam Type', required=True)
    evolution_type = fields.Selection(
        [('normal', 'Normal'), ('grade', 'Grade')],
        'Evolution type', default="normal", required=True)
    venue = fields.Many2one('res.partner', 'Venue')

    @api.constrains('start_date', 'end_date')
    def _check_date_time(self):
        if self.start_date > self.end_date:
            raise ValidationError(_(
                'End Date cannot be set before Start Date.'))

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
