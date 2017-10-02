# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields


class EducationCourse(models.Model):
    _name = 'education.course'

    name = fields.Char('Name', size=32, required=True)
    code = fields.Char('Code', size=8, required=True)
    parent_id = fields.Many2one('education.course', 'Parent Course')
    section = fields.Char('Section', size=32, required=True)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'),
         ('GPA', 'Grade Point Average'),
         ('CWA', 'Course Weighted Average')],
        'Evaluation Type', default="normal", required=True)
    subject_ids = fields.Many2many('education.subject', string='Subject(s)')
    max_unit_load = fields.Float("Maximum Unit Load")
    min_unit_load = fields.Float("Minimum Unit Load")
