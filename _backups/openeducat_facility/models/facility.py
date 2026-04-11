from odoo import fields, models

class OpFacility(models.Model):
    _name = 'op.facility'
    _description = 'Manage Facility'
    name = fields.Char(size=16, required=True)
    code = fields.Char(size=16, required=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_facility_code', 'unique(code)', 'Code should be unique per facility!')]