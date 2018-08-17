# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields
from datetime import datetime


class EducationSession(models.Model):
    _name = 'education.session'
    _inherit = ['mail.thread']
    _rec_name = 'code'

    code = fields.Char(
        string='Code')
    timetable_id = fields.Many2one(
        comodel_name='education.timetable.line',
        string='Timetable Lines')
    date = fields.Date(
        string='Date')
    start_time = fields.Datetime(
        string='Start time',
        compute='_compute_time')
    end_time = fields.Datetime(
        string='End time',
        compute='_compute_time')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('done', 'Done')],
        string='Status',
        default='draft')
    ausence_ids = fields.One2many(
        comodel_name='education.session.ausence',
        inverse_name='session_id',
        string='Ausences')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        index=True,
        track_visibility='onchange',
        default=lambda self: self.env.user)
    teacher_id = fields.Many2one(
        comodel_name='res.partner',
        related='timetable_id.teacher_id',
        string='Teacher')
    subject_id = fields.Many2one(
        comodel_name='education.subject',
        related='timetable_id.subject_id',
        string='Subject')
    group_id = fields.Many2one(
        comodel_name='education.group',
        related='timetable_id.group_id',
        string='Group')
    timerange_id = fields.Many2one(
        comodel_name='education.timerange',
        string='Timerange')

    teacher_assist = fields.Boolean(
            string='Teacher assist')
        

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.session') or 'New'
        return super(EducationSession, self).create(vals)

    @api.depends('date',
                 'timetable_id.timerange_id.start_time',
                 'timetable_id.timerange_id.end_time',
                 )
    def _compute_time(self):
        for session in self:
            if session.timetable_id and session.date:
                start_time = str(
                    session.timetable_id.timerange_id.start_time).split('.')
                end_time = str(
                    session.timetable_id.timerange_id.end_time).split('.')
                date = session.date.split('-')
                session.start_time = datetime(int(date[0]), int(
                    date[1]), int(date[2]),
                    int(start_time[0]) - 1, int(start_time[1]), 0)
                session.end_time = datetime(int(date[0]), int(
                    date[1]), int(date[2]), int(end_time[0]) - 1,
                    int(end_time[1]), 0)
