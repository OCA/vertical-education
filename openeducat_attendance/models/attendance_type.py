from odoo import fields, models

class OpAttendanceType(models.Model):
    _name = 'op.attendance.type'
    _inherit = ['mail.thread']
    _description = 'Attendance Type'
    name = fields.Char(size=20, required=True, tracking=True)
    active = fields.Boolean(default=True)
    present = fields.Boolean('Present ?', tracking=True)
    excused = fields.Boolean('Excused ?', tracking=True)
    absent = fields.Boolean(tracking=True)
    late = fields.Boolean(tracking=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)