# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EducationFaculty(models.Model):
    _name = 'education.faculty'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    faculty_subject_ids = fields.Many2many(
        'education.subject', string='Subject(s)')
    emp_id = fields.Many2one('hr.employee', 'Employee')

    @api.multi
    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'supplier': True, 'employee': True})
