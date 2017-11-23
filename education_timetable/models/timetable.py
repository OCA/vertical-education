# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _
from datetime import timedelta
from odoo.osv import expression


class EducationTimetableLine(models.Model):
    _name = 'education.timetable.line'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Name', required=True, default=lambda self: _('New'))

    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course',
        required=True)

    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group',
        required=True)

    subject_id = fields.Many2one(
        comodel_name='education.subject',
        string='Subject',
        required=True)

    teacher_id = fields.Many2one(
        comodel_name='education.teacher',
        string='Teacher',
        required=True)

    timerange_id = fields.Many2one(
        comodel_name='education.timerange',
        string='Time Range',
        required=True)

    day = fields.Selection(
        [('0', 'Monday'),
         ('1', 'Tuesday'),
         ('2', 'Wednesday'),
         ('3', 'Thursday'),
         ('4', 'Friday')],
        string='Days',
        required=True)

    date_from = fields.Date(
        string='Start Date',
        required=True)

    date_to = fields.Date(
        string='End Date',
        required=True)

    state = fields.Selection(
        [('draft', 'Draft'),
         ('done', 'Done')],
        string='Status',
        default='draft',
        required=True)

    session_ids = fields.One2many(
        comodel_name='education.session',
        inverse_name='timetable_id',
        string='Sessions')

    @api.onchange('course_id')
    def _change_course_id(self):
        if not self.group_id:
            return {'domain': {'subject_id': expression.FALSE_DOMAIN}}
        subject_fields_domain = [
            ('id', 'in', self.course_id.subject_ids.ids)]
        return {'domain': {'subject_id': subject_fields_domain}}

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
        end = fields.Date.from_string(self.date_from)
        start = fields.Date.from_string(self.date_to)
        days = []
        for day in self.get_days(end, start):
            if day.weekday() == int(self.day):
                days.append(day)
        for record in self:
            for day in days:
                session_obj.create({
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
            record.date_from = record.group_id.date_from
            record.date_to = record.group_id.date_to
