# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class EducationGroup(models.Model):
    _inherit = 'education.group'

    faults = fields.Integer(
        string='Number of faults')
    max_faults = fields.Integer(
        string='Number of faults allowed')
    cons_faults = fields.Integer(
        string='Consecutive number of faults')
    max_cons_faults = fields.Integer(
        string='Consecutive number of faults allowed')
