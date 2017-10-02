# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields


class Faculty(models.Model):
    _inherit = 'education.faculty'

    session_ids = fields.One2many(
        'education.session', 'faculty_id', 'Sessions')
