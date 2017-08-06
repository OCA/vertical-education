# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExamRoom(models.Model):
    _name = 'education.exam.room'

    name = fields.Char('Name', size=256, required=True)
    classroom_id = fields.Many2one(
        'education.classroom', 'Classroom', required=True)
    capacity = fields.Integer('Capacity', required=True)

    @api.constrains('capacity')
    def check_capacity(self):
        if self.capacity < 0:
            raise ValidationError(_('Enter proper Capacity'))
        elif self.capacity > self.classroom_id.capacity:
            raise ValidationError(_('Capacity over Classroom capacity!'))

    @api.onchange('classroom_id')
    def onchange_classroom(self):
        self.capacity = self.classroom_id.capacity
