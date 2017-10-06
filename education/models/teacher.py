# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationTeacher(models.Model):
    _name = "education.teacher"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner')
