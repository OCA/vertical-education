# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields


class OpAsset(models.Model):
    _name = 'education.asset'

    asset_id = fields.Many2one('education.classroom', 'Asset')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    code = fields.Char('Code', size=256)
    product_uom_qty = fields.Float('Quantity', required=True)
