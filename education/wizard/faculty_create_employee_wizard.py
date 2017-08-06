# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from openerp import models, fields, api


class WizardEducationFacultyEmployee(models.TransientModel):
    _name = 'wizard.education.faculty.employee'
    _description = "Create Employee and User of Faculty"

    user_boolean = fields.Boolean("Want to create user too ?", default=True)

    @api.multi
    def create_employee(self):
        for record in self:
            active_id = self.env.context.get('active_ids', []) or []
            faculty = self.env['education.faculty'].browse(active_id)
            faculty.create_employee()
            if record.user_boolean and not faculty.user_id:
                user_group = self.env.ref('education.group_education_faculty')
                self.env['res.users'].create_user(faculty, user_group)
