from odoo import api, fields, models

class OpAttendanceLine(models.Model):
    _name = 'op.attendance.line'
    _inherit = ['mail.thread']
    _rec_name = 'attendance_id'
    _description = 'Attendance Lines'
    _order = 'attendance_date desc'
    attendance_id = fields.Many2one('op.attendance.sheet', 'Attendance Sheet', required=True, tracking=True, ondelete='cascade')
    student_id = fields.Many2one('op.student', required=True, tracking=True)
    present = fields.Boolean(tracking=True)
    excused = fields.Boolean('Absent Excused', tracking=True)
    absent = fields.Boolean('Absent Unexcused', tracking=True)
    late = fields.Boolean(tracking=True)
    course_id = fields.Many2one('op.course', related='attendance_id.register_id.course_id', store=True, readonly=True)
    batch_id = fields.Many2one('op.batch', related='attendance_id.register_id.batch_id', store=True, readonly=True)
    remark = fields.Char(size=256, tracking=True)
    attendance_date = fields.Date('Date', related='attendance_id.attendance_date', store=True, readonly=True, tracking=True)
    register_id = fields.Many2one(related='attendance_id.register_id', store=True)
    active = fields.Boolean(default=True)
    attendance_type_id = fields.Many2one('op.attendance.type', required=False, tracking=True)
    state = fields.Selection(related='attendance_id.state')
    _sql_constraints = [('unique_student', 'unique(student_id,attendance_id,attendance_date)', 'Student must be unique per Attendance.')]

    @api.onchange('attendance_type_id')
    def onchange_attendance_type(self):
        if self.attendance_type_id:
            self.present = self.attendance_type_id.present
            self.excused = self.attendance_type_id.excused
            self.absent = self.attendance_type_id.absent
            self.late = self.attendance_type_id.late

    @api.onchange('present')
    def onchange_present(self):
        if self.present:
            self.late = False
            self.excused = False
            self.absent = False

    @api.onchange('absent')
    def onchange_absent(self):
        if self.absent:
            self.present = False
            self.late = False
            self.excused = False

    @api.onchange('excused')
    def onchange_excused(self):
        if self.excused:
            self.present = False
            self.late = False
            self.absent = False

    @api.onchange('late')
    def onchange_late(self):
        if self.late:
            self.present = False
            self.excused = False
            self.absent = False