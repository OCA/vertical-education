

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    teacher = fields.Boolean(
        string='Teacher')
