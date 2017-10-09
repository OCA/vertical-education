# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EducationEnrollment(models.Model):
    _name = "education.enrollment"
    _rec_name = 'code'

    code = fields.Char(
        string='Code', required=True)

    student_id = fields.Many2one(
        comodel_name='education.student',
        string='Student', required=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course', required=True)
    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group', required=True)
    record_id = fields.Many2one(
        comodel_name='education.record',
        string='Record', required=True)

    state = fields.Selection(
        [('pending', 'Pending'),
         ('active', 'Active'),
         ('cancelled', 'Cancelled'),
         ('drop', 'Drop'),
         ('finished', 'Finished')],
        string='Status')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.enrollment') or 'New'
        return super(EducationGroup, self).create(vals)
