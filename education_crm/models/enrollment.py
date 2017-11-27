# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EducationEnrollment(models.Model):
    _inherit = 'education.enrollment'

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead')

    @api.multi
    def action_done(self):
        if self.lead_id:
            self.lead_id.action_set_won()
            super(EducationEnrollment, self).action_done()
