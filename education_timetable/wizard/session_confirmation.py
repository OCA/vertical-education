# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, api


class SessionConfirmation(models.TransientModel):
    _name = 'session.confirmation'
    _description = 'Wizard for Multiple Session Confirmation'

    @api.multi
    def state_confirmation(self):
        active_ids = self.env.context['active_ids']
        lines = self.env['education.session'].search([('id', 'in', active_ids),
                                                      ('state', '=', 'draft')])
        for line in lines:
            line.lecture_confirm()
