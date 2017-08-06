# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, api, fields


class OpHeldExam(models.TransientModel):
    _name = 'education.held.exam'

    course_id = fields.Many2one('education.course', 'Course')
    batch_id = fields.Many2one('education.batch', 'Batch')
    exam_id = fields.Many2one('education.exam', 'Exam')
    subject_id = fields.Many2one('education.subject', 'Subject')
    attendees_line = fields.Many2many(
        'education.exam.attendees', string='Attendees')

    @api.model
    def default_get(self, fields):
        res = super(OpHeldExam, self).default_get(fields)
        active_id = self.env.context.get('active_id', False)
        exam = self.env['education.exam'].browse(active_id)
        session = exam.session_id
        res.update({
            'batch_id': session.batch_id.id,
            'course_id': session.course_id.id,
            'exam_id': active_id,
            'subject_id': exam.subject_id.id
        })
        return res

    @api.multi
    def held_exam(self):
        for record in self:
            if record.attendees_line:
                for attendee in record.attendees_line:
                    attendee.status = 'absent'
            record.exam_id.state = 'held'
            return True
