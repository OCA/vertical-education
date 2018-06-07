# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _


class EducationCourse(models.Model):
    _inherit = 'education.course'

    pack = fields.Boolean(
        string='Pack')
    course_pack_line_ids = fields.Many2many(
        comodel_name='education.course',
        relation='education_course_pack_rel',
        column1='course_id',
        column2='pack_id',
        string='Included Courses')
    course_pack_ids = fields.Many2many(
        comodel_name='education.course',
        relation='education_course_pack_rel',
        column1='pack_id',
        column2='course_id',
        string='Included in Packs')

    # price = fields.Float(
    #     string='Price')
