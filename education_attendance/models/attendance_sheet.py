# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api


class OpAttendanceSheet(models.Model):
    _name = 'education.attendance.sheet'
    _inherit = ['mail.thread']

    @api.multi
    @api.depends('attendance_line.present')
    def _compute_total_present(self):
        for record in self:
            record.total_present = self.env['education.attendance.line'].search_count(
                [('present', '=', True), ('attendance_id', '=', record.id)])

    @api.multi
    @api.depends('attendance_line.present')
    def _compute_total_absent(self):
        for record in self:
            record.total_absent = self.env['education.attendance.line'].search_count(
                [('present', '=', False), ('attendance_id', '=', record.id)])

    name = fields.Char('Name', required=True, size=32)
    register_id = fields.Many2one(
        'education.attendance.register', 'Register', required=True,
        track_visibility="onchange")
    course_id = fields.Many2one(
        'education.course', related='register_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'education.batch', 'Batch', related='register_id.batch_id', store=True,
        readonly=True)
    session_id = fields.Many2one('education.session', 'Session')
    attendance_date = fields.Date(
        'Date', required=True, default=lambda self: fields.Date.today(),
        track_visibility="onchange")
    attendance_line = fields.One2many(
        'education.attendance.line', 'attendance_id', 'Attendance Line')
    total_present = fields.Integer(
        'Total Present', compute='_compute_total_present',
        track_visibility="onchange")
    total_absent = fields.Integer(
        'Total Absent', compute='_compute_total_absent',
        track_visibility="onchange")
    faculty_id = fields.Many2one('education.faculty', 'Faculty')

    _sql_constraints = [
        ('unique_register_sheet',
         'unique(register_id,session_id,attendance_date)',
         'Sheet must be unique per Register/Session.'),
    ]
