# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationStudent(models.Model):
    _name = "education.student"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner')
    record_ids = fields.One2many(
        'education.record',
        'student_id',
        'Academic Records')