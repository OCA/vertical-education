from odoo import fields, models

class OpFacilityLine(models.Model):
    _inherit = 'op.facility.line'
    classroom_id = fields.Many2one('op.classroom')
    _sql_constraints = [('unique_facility_classroom', 'UNIQUE(facility_id, classroom_id)', 'Facility name exists. Please choose a unique name or update the quantity.')]