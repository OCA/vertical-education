# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api


class OpClassroom(models.Model):
    _name = 'education.classroom'

    name = fields.Char('Name', size=16, required=True)
    code = fields.Char('Code', size=4, required=True)
    course_id = fields.Many2one('education.course', 'Course')
    batch_id = fields.Many2one('education.batch', 'Batch')
    capacity = fields.Integer(string='No of Person')
    facilities = fields.One2many(
        'education.facility.line', 'classroom_id', string='Facility Lines')
    asset_line = fields.One2many('education.asset', 'asset_id', 'Asset')

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
