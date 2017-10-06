# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationCourseCategory(models.Model):
    _name = "education.course.category"

    name = fields.Char()


class EducationSubject(models.Model):
    _name = "education.subject"

    name = fields.Char()


class EducationCourse(models.Model):
    _name = "education.course"

    name = fields.Char()
    code = fields.Char()
    category_id = fields.Many2one(
        comodel_name='education.category',
        string='Category')
    subject_ids = fields.Many2many(
        comodel_name='education.subject',
        string='Subjects')
