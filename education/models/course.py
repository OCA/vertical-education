# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationCourseCategory(models.Model):
    _name = "education.course.category"
    _description = "Course Category"
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _rec_name = 'complete_name'
    _order = 'parent_left'

    name = fields.Char(
        string='Name',
        index=True,
        required=True,
        translate=True)
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True)
    parent_id = fields.Many2one(
        comodel_name='education.course.category',
        string='Parent Category',
        index=True,
        ondelete='cascade')
    child_id = fields.One2many(
        comodel_name='education.course.category',
        inverse_name='parent_id',
        string='Child Categories')
    parent_left = fields.Integer(
        string='Left Parent',
        index=1)
    parent_right = fields.Integer(
        'Right Parent',
        index=1)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name


class EducationSubject(models.Model):
    _name = "education.subject"
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True)

    course_ids = fields.Many2many(
        comodel_name='education.course',
        relation='course_subject_rel',
        column1='subject_id',
        column2='course_id',
        string='Courses')


class EducationCourse(models.Model):
    _name = "education.course"
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Name',
        required=True)
    code = fields.Char(
        string='Code',
        required=True)
    category_id = fields.Many2one(
        comodel_name='education.course.category',
        string='Category')
    subject_ids = fields.Many2many(
        comodel_name='education.subject',
        relation='course_subject_rel',
        column1='course_id',
        column2='subject_id',
        string='Subjects')

    duration = fields.Float(
        string='Duration',
        company_dependent=True)

    active = fields.Boolean(
        string='Active', default=True)
