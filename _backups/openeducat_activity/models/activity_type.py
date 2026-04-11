from odoo import fields, models

class OpActivityType(models.Model):
    _name = 'op.activity.type'
    _description = 'Activity Type'
    name = fields.Char(size=128, required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_name', 'unique(name)', 'Activity type must be unique!')]