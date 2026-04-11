from odoo import fields, models

class OpMediaType(models.Model):
    _name = 'op.media.type'
    _description = 'Media Type'
    name = fields.Char(size=64, required=True)
    code = fields.Char(size=64, required=True)
    _sql_constraints = [('unique_media_type_code', 'unique(code)', 'Code should be unique per media type!')]