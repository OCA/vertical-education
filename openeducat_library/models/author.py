from odoo import fields, models

class OpAuthor(models.Model):
    _name = 'op.author'
    _description = 'Media Author'
    name = fields.Char(size=128, required=True)
    address = fields.Many2one('res.partner')
    media_ids = fields.Many2many('op.media', string='Media(s)')