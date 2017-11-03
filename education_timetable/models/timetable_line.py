# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _
from datetime import timedelta


class EducationTimetableLine(models.Model):
    _name = 'education.timetable.line'

    name = fields.Char(
        string='Name', required=True, default=lambda self: _('New'))

    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course')

    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group')

    subject_id = fields.Many2one(
        comodel_name='education.subject',
        string='Subject')

    teacher_id = fields.Many2one(
        comodel_name='education.teacher',
        string='Teacher')

    timerange_id = fields.Many2one(
        comodel_name='education.timerange',
        string='Time Range')

    day = fields.Selection(
        [('0', 'Monday'),
         ('1', 'Tuesday'),
         ('2', 'Wednesday'),
         ('3', 'Thursday'),
         ('4', 'Friday')],
        string='Days')

    start_date = fields.Datetime(
        string='Start Date')

    end_date = fields.Datetime(
        string='End Date')

    state = fields.Selection(
        [('draft', 'Draft'),
         ('done', 'Done')],
        string='Status',
        default='draft')

    session_ids = fields.One2many(
        comodel_name='education.session',
        inverse_name='timetable_id',
        string='Sessions')

    @api.multi
    def get_days(self, start, end):
        step = timedelta(days=1)
        for i in range((end - start).days):
            yield start + i * step

    @api.multi
    def generate_new_sessions(self):
        self.ensure_one()
        self.state = 'done'
        session_obj = self.env['education.session']
        end = fields.Date.from_string(self.start_date)
        start = fields.Date.from_string(self.end_date)
        days = []
        for day in self.get_days(end, start):
            if day.weekday() == int(self.days):
                days.append(day)
        for record in self:
            for day in days:
                session_id = session_obj.create({
                    'timetable_id': record.id,
                    'date': day
                })

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'education.timetable.line') or 'New'
        return super(EducationTimetableLine, self).create(vals)

    @api.onchange('group_id')
    def _onchange_group_id(self):
        for record in self:
            record.start_date = record.group_id.date_from
            record.end_date = record.group_id.date_to
