from odoo import fields, models

class OpStudent(models.Model):
    _inherit = 'op.student'
    activity_log = fields.One2many('op.activity', 'student_id')
    activity_count = fields.Integer(compute='_compute_count')

    def get_activity(self):
        action = self.env.ref('openeducat_activity.act_open_op_activity_view').sudo().read()[0]
        action['domain'] = [('student_id', 'in', self.ids)]
        return action

    def _compute_count(self):
        for record in self:
            record.activity_count = self.env['op.activity'].search_count([('student_id', 'in', self.ids)])