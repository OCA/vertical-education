from odoo import api, fields, models

class OpHeldExam(models.TransientModel):
    _name = 'op.held.exam'
    _description = 'Held Exam'
    course_id = fields.Many2one('op.course')
    batch_id = fields.Many2one('op.batch')
    exam_id = fields.Many2one('op.exam')
    subject_id = fields.Many2one('op.subject')
    attendees_line = fields.Many2many('op.exam.attendees', string='Attendees')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get('active_id', False)
        exam = self.env['op.exam'].browse(active_id)
        session = exam.session_id
        res.update({'batch_id': session.batch_id.id, 'course_id': session.course_id.id, 'exam_id': active_id, 'subject_id': exam.subject_id.id})
        return res

    def held_exam(self):
        for record in self:
            if record.attendees_line:
                for attendee in record.attendees_line:
                    attendee.status = 'absent'
            record.exam_id.state = 'held'
            return True