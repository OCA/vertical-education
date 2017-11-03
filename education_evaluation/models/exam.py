# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _


class EducationExam(models.Model):
    _name = 'education.exam'

    name = fields.Char(
        string='Name',
        compute='_compute_name', readonly=True)

    state = fields.Selection(
        [('draft', 'Draft'),
         ('planned', 'Planned'),
         ('done', 'Done')],
        string='Status',
        default="draft")

    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group')

    subject_id = fields.Many2one(
        comodel_name='education.subject',
        string='Subject')

    result_ids = fields.One2many(
        comodel_name='education.result',
        inverse_name='exam_id',
        string='Results')

    date = fields.Date(
        string='Date')

    @api.multi
    def _compute_name(self):
        for record in self:
            record.name = record.group_id.name + \
                '/' + record.subject_id.name + '/' + record.date

    @api.multi
    def set_planned(self):
        self.ensure_one()
        self.state = 'planned'
        values = []
        for record_subject in self.group_id.enrollment_ids.mapped(
                'record_id.record_subject_ids').filtered(
                    lambda r: r.subject_id == self.subject_id
        ):
            values.append((0, 0, {
                'record_subject_id': record_subject and record_subject.id}))
        self.result_ids = values

    @api.multi
    def set_done(self):
        self.state = 'done'
