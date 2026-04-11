from odoo import fields, models

class OpTag(models.Model):
    _name = 'op.tag'
    _description = 'Media Tags'
    name = fields.Char(size=64, required=True)