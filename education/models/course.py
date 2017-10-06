# -*- coding: utf-8 -*-

from odoo import models, fields


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
        string='Category', required=True)
    subject_ids = fields.Many2many(
        comodel_name='education.subject',
        string='Subjects')
