# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationGroup(models.Model):
    _name = "education.group"

    name = fields.Char()
    code = fields.Char()
    course_id = fields.Many2one(
        comodel_name='education.course')
    record_id = fields.Many2one(
        comodel_name='education.record',
        string='Record')
    date_from = fields.Date()
    date_to = fields.Date()
