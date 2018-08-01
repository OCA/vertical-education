# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api


class EducationSessionPresence(models.TransientModel):
    _name = 'education.session.presence'

    session_id = fields.Many2one(
        comodel_name='education.session',
        string='Session')

    session_presence_ids = fields.One2many(
        comodel_name='education.session.presence.line',
        inverse_name='presence_id',
        string='Session Presence')

    @api.onchange('session_id')
    def _onchange_session_students(self):
        lines = []
        enrollments = self.session_id.timetable_id.group_id.enrollment_ids
        for enroll in enrollments.filtered(lambda e: e.state == 'done'):
            lines.append((0, 0, {'student_id': enroll.student_id.id}))
        self.session_presence_ids = lines

    @api.multi
    def create_ausences(self):
        values = []
        self.ensure_one()
        record_subject_obj = self.env['education.record.subject']
        students = self.session_id.ausence_ids.mapped('student_id')
        for line in self.session_presence_ids.filtered(
                lambda l: l.lack):
            if line.student_id not in students:
                timetable_id = line.presence_id.session_id.timetable_id
                course_id = timetable_id.group_id.course_id.id
                subject_id = timetable_id.subject_id.id
                student_id = line.student_id.id
                record_subject = record_subject_obj.search([
                    ('course_id', '=', course_id),
                    ('student_id', '=', student_id),
                    ('subject_id', '=', subject_id),
                ])
                ausence_values = ({
                    'session_id': self.env.context.get('active_id'),
                    'student_id': line.student_id.id,
                    'record_subject_id': record_subject and record_subject.id,
                    'notes': line.notes,
                })
                values.append((0, 0, ausence_values))
            else:
                self.session_id.ausence_ids.filtered(
                    lambda l: l.student_id == line.student_id).write({
                        'notes': line.notes
                    })
        self.session_id.ausence_ids = values
        self.session_id.state = 'done'
