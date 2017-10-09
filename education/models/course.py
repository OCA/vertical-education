# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EducationCourseCategory(models.Model):
    _name = "education.course.category"

    name = fields.Char(string='Name', required=True)


class EducationSubject(models.Model):
    _name = "education.subject"

    name = fields.Char(string='Name', required=True)


class EducationCourse(models.Model):
    _name = "education.course"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    category_id = fields.Many2one(
        comodel_name='education.course.category',
        string='Category')
    subject_ids = fields.Many2many(
        comodel_name='education.subject',
        string='Subjects')

    state = fields.Selection(
        [('active', 'Active'),
         ('cancelled', 'Cancelled')],
        string='Status',
        default="active")

    @api.multi
    def do_toggle_cancelled(self):
        self.state = 'cancelled'
