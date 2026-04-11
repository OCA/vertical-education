from odoo import api, fields, models

class OpFaculty(models.Model):
    _inherit = 'op.faculty'
    session_ids = fields.One2many('op.session', 'faculty_id', 'Sessions')
    session_count = fields.Integer(compute='_compute_session_details')

    @api.depends('session_ids')
    def _compute_session_details(self):
        for session in self:
            session.session_count = self.env['op.session'].search_count([('faculty_id', '=', self.id)])

    def count_sessions_details(self):
        return {'type': 'ir.actions.act_window', 'name': 'Sessions', 'view_mode': 'list,form', 'res_model': 'op.session', 'domain': [('faculty_id', '=', self.id)], 'target': 'current'}