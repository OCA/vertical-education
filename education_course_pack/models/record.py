# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _


class EducationRecord(models.Model):
    _inherit = "education.record"

    pack = fields.Boolean(
        string='Pack',
        related='course_id.pack')
    parent_record_id = fields.Many2one(
        comodel_name='education.record',
        string='Parent Record')
    pack_record_ids = fields.One2many(
        comodel_name='education.record',
        inverse_name='parent_record_id',
        string='Pack Record')
