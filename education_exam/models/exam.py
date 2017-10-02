# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExam(models.Model):
    _name = 'education.exam'
    _inherit = 'mail.thread'
    _description = 'Exam'

    session_id = fields.Many2one('education.exam.session', 'Exam Session')
    subject_id = fields.Many2one('education.subject', 'Subject', required=True)
    exam_code = fields.Char('Exam Code', size=8, required=True)
    attendees_line = fields.One2many(
        'education.exam.attendees', 'exam_id', 'Attendees', readonly=True)
    start_time = fields.Datetime('Start Time', required=True)
    end_time = fields.Datetime('End Time', required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('schedule', 'Scheduled'), ('held', 'Held'),
         ('result_updated', 'Result Updated'),
         ('cancel', 'Cancelled'), ('done', 'Done')], 'State',
        readonly=True, default='draft', track_visibility='onchange')
    note = fields.Text('Note')
    responsible_id = fields.Many2many(
        'education.faculty', string='Responsible')
    name = fields.Char('Exam', size=256, required=True)
    total_marks = fields.Integer('Total Marks', required=True)
    min_marks = fields.Integer('Passing Marks', required=True)

    @api.constrains('total_marks', 'min_marks')
    def _check_marks(self):
        if self.total_marks <= 0.0 or self.min_marks <= 0.0:
            raise ValidationError(_('Enter proper marks!'))
        if self.min_marks > self.total_marks:
            raise ValidationError(_(
                "Passing Marks can't be greater than Total Marks"))

    @api.constrains('start_time', 'end_time')
    def _check_date_time(self):
        if self.start_time > self.end_time:
            raise ValidationError(_('End Time cannot be set \
            before Start Time.'))

    @api.multi
    def act_result_updated(self):
        self.state = 'result_updated'

    @api.multi
    def act_done(self):
        self.state = 'done'

    @api.multi
    def act_draft(self):
        self.state = 'draft'

    @api.multi
    def act_cancel(self):
        self.state = 'cancel'
