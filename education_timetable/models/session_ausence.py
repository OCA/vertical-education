# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _


class EducationSessionAusence(models.Model):
    _name = 'education.session.ausence'

    session_id = fields.Many2one(
        comodel_name='education.session',
        string='Session')

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student')

    notes = fields.Char(
        string='Notes')

    supporting_document = fields.Boolean(
        string='Supporting Document')
