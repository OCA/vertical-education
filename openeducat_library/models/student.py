from odoo import api, fields, models

class OpStudent(models.Model):
    _inherit = 'op.student'
    library_card_id = fields.Many2one('op.library.card')
    media_movement_lines = fields.One2many('op.media.movement', 'student_id', 'Movements')
    media_movement_lines_count = fields.Integer(compute='_compute_media_movement_lines')

    @api.depends('media_movement_lines')
    def _compute_media_movement_lines(self):
        for media in self:
            media.media_movement_lines_count = self.env['op.media.movement'].search_count([('student_id', '=', self.id)])

    def count_media_movement_lines(self):
        return {'type': 'ir.actions.act_window', 'name': 'Media Movement', 'view_mode': 'list,form', 'res_model': 'op.media.movement', 'domain': [('student_id', '=', self.id)], 'target': 'current'}