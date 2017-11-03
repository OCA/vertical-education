# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _


class EducationSessionPresence(models.TransientModel):
    _name = 'education.session.presence'

    session_id = fields.Many2one(
        comodel_name='education.session',
        string='Session')

    session_presence_ids = fields.One2many(
        comodel_name='education.session.presence.line',
        inverse_name='presence_id',
        string='Session Presence')

    # @api.model
    # def default_get(self, fields):
    #     res = super(EducationSessionPresence, self).default_get(fields)
    #     session_id = self.env.context.get('active_id')
    #     session = self.env['education.session'].browse(session_id)
    #     lines = []
    #     for record in self.session_id.timetable_id.group_id.record_ids:
    #             values.append((0,0,{'student_id': record.student_id.id}))
    #     self.session_presence_ids = lines
    #     res['session_presence_ids'] = lines
    #     return res

    @api.onchange('session_id')
    def _onchange_session_students(self):
        lines = []
        for record in self.session_id.timetable_id.group_id.record_ids:
            lines.append((0, 0, {'student_id': record.student_id.id}))
        self.session_presence_ids = lines

    @api.multi
    def create_ausences(self):
        values = []
        students = self.session_id.ausence_ids.mapped('student_id')
        for line in self.session_presence_ids.filtered(
                lambda l: l.lack):
            if line.student_id not in students:
                ausence_values = ({
                    'session_id': self.env.context.get('active_id'),
                    'student_id': line.student_id.id,
                    'notes': line.notes,
                })
                values.append((0, 0, ausence_values))
            else:
                self.session_id.ausence_ids.filtered(lambda l: l.student_id == line.student_id).write({
                    'notes': line.notes
                })
        self.session_id.ausence_ids = values
