from odoo import fields, models

class OpActivity(models.Model):
    _name = 'op.activity'
    _description = 'Student Activity'
    _rec_name = 'student_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_faculty(self):
        return self.env['op.faculty'].search([('user_id', '=', self._uid)], limit=1) or False
    student_id = fields.Many2one('op.student', required=True)
    faculty_id = fields.Many2one('op.faculty', default=lambda self: self._default_faculty())
    type_id = fields.Many2one('op.activity.type', 'Activity Type')
    description = fields.Text()
    date = fields.Date(default=fields.Date.today())
    active = fields.Boolean(default=True)