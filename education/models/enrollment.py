# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationEnrollment(models.Model):
    _name = "education.enrollment"
    _rec_name = 'code'

    code = fields.Char(
        string='Code', required=True)
    name = fields.Char(
        string='Name', required=True)

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student', required=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course', required=True)
    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group', required=True)
