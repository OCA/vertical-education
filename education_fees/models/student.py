# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)


from odoo import models, api


class EducationStudent(models.Model):
    _inherit = 'education.student'

    @api.multi
    def open_partner_history(self):
        self.ensure_one()
        return self.partner_id.open_partner_history()


class EducationFaculty(models.Model):
    _inherit = 'education.faculty'

    @api.multi
    def open_partner_history(self):
        self.ensure_one()
        return self.partner_id.open_partner_history()
