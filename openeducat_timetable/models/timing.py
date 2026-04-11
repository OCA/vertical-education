from odoo import fields, models

class OpTiming(models.Model):
    _name = 'op.timing'
    _description = 'Period'
    _order = 'sequence'
    name = fields.Char(size=16, required=True)
    hour = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], 'Hours', required=True)
    minute = fields.Selection([('00', '00'), ('15', '15'), ('30', '30'), ('45', '45')], required=True)
    duration = fields.Float()
    am_pm = fields.Selection([('am', 'AM'), ('pm', 'PM')], 'AM/PM', required=True)
    sequence = fields.Integer()