# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields


class OpExamType(models.Model):
    _name = 'education.exam.type'

    name = fields.Char('Name', size=256, required=True)
    code = fields.Char('Code', size=4, required=True)
