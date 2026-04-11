from odoo import fields, models

class OpPublisher(models.Model):
    _name = 'op.publisher'
    _description = 'Publisher'
    name = fields.Char(size=20, required=True)
    address_id = fields.Many2one('res.partner')
    media_ids = fields.Many2many('op.media', string='Media(s)')