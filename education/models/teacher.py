# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EducationTeacher(models.Model):
    _name = "education.teacher"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee')

    @api.multi
    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'address_home_id': record.partner_id.id
            }
            employee_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': employee_id.id})
            record.partner_id.write({'supplier': True, 'employee': True})
