# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from openerp import models, fields, api


class WizardEducationStudent(models.TransientModel):
    _name = 'wizard.education.student'
    _description = "Create User for selected Student(s)"

    def _get_students(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    student_ids = fields.Many2many(
        'education.student', default=_get_students, string='Students')

    @api.multi
    def create_student_user(self):
        user_group = self.env.ref('education.group_education_student')
        active_ids = self.env.context.get('active_ids', []) or []
        records = self.env['education.student'].browse(active_ids)
        self.env['res.users'].create_user(records, user_group)
