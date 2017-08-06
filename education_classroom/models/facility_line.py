# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields


class OpFacilityLine(models.Model):

    _inherit = 'education.facility.line'

    classroom_id = fields.Many2one('education.classroom', 'Classroom')
