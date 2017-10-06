# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationRecord(models.Model):
    _name = "education.record"

    name = fields.Char(
        string='Name', required=True)

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student', required=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course', required=True)
    group_ids = fields.One2many(
        comodel_name='education.group',
        inverse_name='record_id',
        string='Groups')
