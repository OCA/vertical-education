# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import calendar
import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

week_days = [(calendar.day_name[0], _(calendar.day_name[0])),
             (calendar.day_name[1], _(calendar.day_name[1])),
             (calendar.day_name[2], _(calendar.day_name[2])),
             (calendar.day_name[3], _(calendar.day_name[3])),
             (calendar.day_name[4], _(calendar.day_name[4])),
             (calendar.day_name[5], _(calendar.day_name[5])),
             (calendar.day_name[6], _(calendar.day_name[6]))]


class Session(models.Model):
    _name = 'education.session'
    _inherit = ['mail.thread']
    _description = 'Sessions'
    _rec_name = 'name'

    name = fields.Char(compute='_compute_name', string='Name', store=True)
    timing_id = fields.Many2one(
        'education.timing', 'Timing', required=True, track_visibility="onchange")
    start_datetime = fields.Datetime(
        'Start Time', required=True,
        default=lambda self: fields.Datetime.now())
    end_datetime = fields.Datetime(
        'End Time', required=True)
    course_id = fields.Many2one(
        'education.course', 'Course', required=True)
    faculty_id = fields.Many2one(
        'education.faculty', 'Faculty', required=True)
    batch_id = fields.Many2one(
        'education.batch', 'Batch', required=True)
    subject_id = fields.Many2one(
        'education.subject', 'Subject', required=True)
    classroom_id = fields.Many2one(
        'education.classroom', 'Classroom')
    color = fields.Integer('Color Index')
    type = fields.Selection(week_days, 'Days', translate=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('done', 'Done'), ('cancel', 'Canceled')],
        'Status', default='draft')
    user_ids = fields.Many2many(
        'res.users', compute='_compute_batch_users',
        store=True, string='Users')

    @api.multi
    @api.depends('faculty_id', 'subject_id', 'start_datetime')
    def _compute_name(self):
        for session in self:
            session.name = session. faculty_id.name + ':' + \
                session.subject_id.name + ':' + str(session.start_datetime)

    # For record rule on student and faculty dashboard
    @api.multi
    @api.depends('batch_id', 'faculty_id')
    def _compute_batch_users(self):
        for session in self:
            usr = []
            students = self.env['education.student'].search(
                [('course_detail_ids.batch_id', '=', session.batch_id.id)])
            for x in students:
                if x.user_id:
                    usr.append(x.user_id.id)
            if session.faculty_id.user_id:
                usr.append(session.faculty_id.user_id.id)
            session.user_ids = usr

    @api.multi
    def lecture_draft(self):
        self.state = 'draft'

    @api.multi
    def lecture_confirm(self):
        self.state = 'confirm'

    @api.multi
    def lecture_done(self):
        self.state = 'done'

    @api.multi
    def lecture_cancel(self):
        self.state = 'cancel'

    @api.constrains('start_datetime', 'end_datetime')
    def _check_date_time(self):
        if self.start_datetime > self.end_datetime:
            raise ValidationError(_(
                'End Time cannot be set before Start Time.'))

    @api.model
    def create(self, values):
        res = super(Session, self).create(values)
        mfids = res.message_follower_ids
        partner_val = []
        partner_ids = []
        for val in mfids:
            partner_val.append(val.partner_id.id)
        if res.faculty_id and res.faculty_id.user_id:
            partner_ids.append(res.faculty_id.user_id.partner_id.id)
        if res.batch_id and res.course_id:
            course_val = self.env['education.student.course'].search([
                ('batch_id', '=', res.batch_id.id),
                ('course_id', '=', res.course_id.id)
            ])
            for val in course_val:
                if val.student_id.user_id:
                    partner_ids.append(val.student_id.user_id.partner_id.id)
        subtype_id = self.env['mail.message.subtype'].sudo().search([
            ('name', '=', 'Discussions')])
        if partner_ids and subtype_id:
            for partner in partner_ids:
                if partner in partner_val:
                    continue
                val = self.env['mail.followers'].sudo().create({
                    'res_model': res._name,
                    'res_id': res.id,
                    'partner_id': partner,
                    'subtype_ids': [[6, 0, [subtype_id[0].id]]]
                })
        return res

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False

    @api.onchange('start_datetime')
    def onchange_start_date(self):
        start_datetime = datetime.datetime.strptime(
            self.start_datetime, "%Y-%m-%d %H:%M:%S")
        if start_datetime and start_datetime.weekday() == 0:
            self.type = calendar.day_name[0]
        elif start_datetime and start_datetime.weekday() == 1:
            self.type = calendar.day_name[1]
        elif start_datetime and start_datetime.weekday() == 2:
            self.type = calendar.day_name[2]
        elif start_datetime and start_datetime.weekday() == 3:
            self.type = calendar.day_name[3]
        elif start_datetime and start_datetime.weekday() == 4:
            self.type = calendar.day_name[4]
        elif start_datetime and start_datetime.weekday() == 5:
            self.type = calendar.day_name[5]

    @api.multi
    def notify_user(self):
        for session in self:
            template = self.env.ref(
                'education_timetable.session_details_changes',
                raise_if_not_found=False)
            template.send_mail(session.id)

    @api.multi
    def get_emails(self, follower_ids):
        email_ids = ''
        for user in follower_ids:
            if email_ids:
                email_ids = email_ids + ',' + str(user.partner_id.email)
            else:
                email_ids = str(user.partner_id.email)
        return email_ids

    @api.multi
    def get_subject(self):
        return 'lacture of ' + self.faculty_id.name + \
            ' for ' + self.subject_id.name + ' is ' + self.state

    @api.multi
    @api.model
    def write(self, vals):
        data = super(Session,
                     self.with_context(check_move_validity=False)).write(vals)
        if self.state not in ('draft', 'done'):
            self.notify_user()
        return data
