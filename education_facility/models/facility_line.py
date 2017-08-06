# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpFacilityLine(models.Model):
    _name = 'education.facility.line'
    _rec_name = 'facility_id'

    facility_id = fields.Many2one('education.facility', 'Facility',
                                  required=True)
    quantity = fields.Float('Quantity', required=True)

    @api.constrains('quantity')
    def check_quantity(self):
        if self.quantity <= 0.0:
            raise ValidationError(_("Enter proper Quantity in Facilities!"))
