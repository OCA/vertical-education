# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _


class WizardCrmPostponed(models.TransientModel):
    _name = 'wizard.crm.postponed'

    tag_ids = fields.Many2many(
        comodel_name='education.crm.tags',
        string='Postponed tags')

    @api.multi
    def action_postponed_tag(self):
        crm = self.env['crm.lead']\
            .browse(self.env.context.get('active_id'))
        crm_stage_id = self.env['crm.stage'].search([
            ('name', '=', 'Pospuesto')
        ])
        crm.tag_pos_ids = self.tag_ids.ids
        crm.stage_id = crm_stage_id.id
        crm.stage = True
