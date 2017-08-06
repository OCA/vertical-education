# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api


class OpAttendanceRegister(models.Model):
    _name = 'education.attendance.register'

    name = fields.Char('Name', size=16, required=True)
    code = fields.Char('Code', size=8, required=True)
    course_id = fields.Many2one('education.course', 'Course', required=True)
    batch_id = fields.Many2one('education.batch', 'Batch', required=True)
    subject_id = fields.Many2one('education.subject', 'Subject')

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
