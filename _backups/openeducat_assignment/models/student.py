from odoo import fields, models

class OpStudent(models.Model):
    _inherit = 'op.student'
    allocation_ids = fields.Many2many('op.assignment', string='Assignment(s)')
    assignment_count = fields.Integer(compute='_compute_count_assignment')

    def get_assignment(self):
        action = self.env.ref('openeducat_assignment.act_open_op_assignment_view').sudo().read()[0]
        action['domain'] = [('allocation_ids', 'in', self.ids)]
        return action

    def _compute_count_assignment(self):
        for record in self:
            record.assignment_count = self.env['op.assignment'].search_count([('allocation_ids', 'in', self.ids)])