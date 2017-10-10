# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EducationRecord(models.Model):
    _name = "education.record"

    code = fields.Char(
        string='Code', required=True, default=lambda self: _('New'))

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student', required=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course', required=True)
    # group_ids = fields.One2many(
    #     comodel_name='education.group',
    #     inverse_name='record_ids',
    #     string='Groups')

    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group')

    state = fields.Selection(
        [('active', 'Active'),
         ('done', 'Done'),
         ('cancelled', 'Cancelled')],
        string='Status',
        default="active")

    _sql_constraints = [
        ('unique_course_record_id',
         'unique(course_id,group_id,student_id)',
         'Student must be unique per Record!'),
    ]
