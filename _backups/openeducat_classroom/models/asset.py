from odoo import fields, models

class OpAsset(models.Model):
    _name = 'op.asset'
    _description = 'Classroom Assets'
    asset_id = fields.Many2one('op.classroom')
    product_id = fields.Many2one('product.product', required=True)
    code = fields.Char(size=256)
    product_uom_qty = fields.Float('Quantity', required=True)