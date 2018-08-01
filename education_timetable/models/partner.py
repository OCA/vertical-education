# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ausence_ids = fields.One2many(
        comodel_name='education.session.ausence',
        inverse_name='student_id',
        string='Ausences')

    session_ids = fields.One2many(
        comodel_name='education.session',
        inverse_name='teacher_id',
        string='Sessions')
