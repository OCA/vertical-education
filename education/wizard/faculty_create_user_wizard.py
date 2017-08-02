# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from openerp import models, fields, api


class WizardEducationFaculty(models.TransientModel):
    _name = 'wizard.education.faculty'
    _description = "Create User for selected Faculty(s)"

    def _get_faculties(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    faculty_ids = fields.Many2many(
        'education.faculty', default=_get_faculties, string='Faculties')

    @api.multi
    def create_faculty_user(self):
        user_group = self.env.ref('education.group_education_faculty')
        active_ids = self.env.context.get('active_ids', []) or []
        records = self.env['education.faculty'].browse(active_ids)
        self.env['res.users'].create_user(records, user_group)
