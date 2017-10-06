# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationGroup(models.Model):
    _name = "education.group"

    name = fields.Char(
        string='Name', required=True)

    code = fields.Char(
        string='Code', required=True)

    course_id = fields.Many2one(
        comodel_name='education.course', required=True)
    record_id = fields.Many2one(
        comodel_name='education.record',
        string='Record', required=True)
    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
