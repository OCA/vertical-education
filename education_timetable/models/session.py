# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _


class EducationSession(models.Model):
    _name = 'education.session'

    code = fields.Char(
        string='Code')

    timetable_id = fields.Many2one(
        comodel_name='education.timetable.line',
        string='Timetable Lines')

    date = fields.Date(
        string='Date')

    state = fields.Selection(
        [('draft', 'Draft'),
         ('done', 'Done')],
        string='Status',
        default='draft')

    ausence_ids = fields.One2many(
        comodel_name='education.session.ausence',
        inverse_name='session_id',
        string='Ausences')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.session') or 'New'
        return super(EducationSession, self).create(vals)
