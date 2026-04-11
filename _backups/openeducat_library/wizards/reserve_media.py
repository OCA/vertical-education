from odoo import fields, models

class ReserveMedia(models.TransientModel):
    """Reserve Media"""
    _name = 'reserve.media'
    _description = 'Media Reserve'
    partner_id = fields.Many2one('res.partner', required=True)

    def set_partner(self):
        for media in self:
            self.env['op.media.movement'].browse(self.env.context.get('active_ids', False)).write({'partner_id': media.partner_id.id, 'reserver_name': media.partner_id.name, 'state': 'reserve'})