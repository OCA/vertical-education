# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from openerp import models, fields, api


class WizardOpStudent(models.TransientModel):
    _name = 'wizard.op.student'
    _description = "Create User for selected Student(s)"

    def _get_students(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    student_ids = fields.Many2many(
        'op.student', default=_get_students, string='Students')

    @api.multi
    def create_student_user(self):
        user_group = self.env.ref('education.group_op_student')
        active_ids = self.env.context.get('active_ids', []) or []
        records = self.env['op.student'].browse(active_ids)
        self.env['res.users'].create_user(records, user_group)
