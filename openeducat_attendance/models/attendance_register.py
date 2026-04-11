from odoo import api, fields, models

class OpAttendanceRegister(models.Model):
    _name = 'op.attendance.register'
    _inherit = ['mail.thread']
    _description = 'Attendance Register'
    _order = 'id DESC'
    name = fields.Char(size=16, required=True, tracking=True)
    code = fields.Char(size=16, required=True, tracking=True)
    course_id = fields.Many2one('op.course', required=True, tracking=True)
    batch_id = fields.Many2one('op.batch', required=True, tracking=True)
    subject_id = fields.Many2one('op.subject', tracking=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_attendance_register_code', 'unique(code)', 'Code should be unique per attendance register!')]

    @api.depends('course_id')
    def onchange_course(self):
        if not self.course_id:
            self.batch_id = False