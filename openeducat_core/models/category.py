from odoo import fields, models

class OpCategory(models.Model):
    _name = 'op.category'
    _description = 'OpenEduCat Category'
    name = fields.Char(size=256, required=True)
    code = fields.Char(size=16, required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    _sql_constraints = [('unique_category_code', 'unique(code)', 'Code should be unique per category!')]