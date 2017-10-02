# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExamAttendees(models.Model):
    _name = 'education.exam.attendees'
    _rec_name = 'student_id'

    student_id = fields.Many2one('education.student', 'Student', required=True)
    status = fields.Selection(
        [('present', 'Present'), ('absent', 'Absent')],
        'Status', default="present", required=True)
    marks = fields.Integer('Marks')
    note = fields.Text('Note')
    exam_id = fields.Many2one('education.exam', 'Exam', required=True)
    course_id = fields.Many2one('education.course', 'Course', readonly=True)
    batch_id = fields.Many2one('education.batch', 'Batch', readonly=True)
    room_id = fields.Many2one('education.exam.room', 'Room')

    _sql_constraints = [
        ('unique_attendees',
         'unique(student_id,exam_id)',
         'Attendee must be unique per exam.'),
    ]

    @api.onchange('exam_id')
    def onchange_exam(self):
        self.course_id = self.exam_id.session_id.course_id
        self.batch_id = self.exam_id.session_id.batch_id
        self.student_id = False

    @api.constrains('marks')
    def _check_marks(self):
        if self.marks < 0.0:
            raise ValidationError(_("Enter proper marks!"))
