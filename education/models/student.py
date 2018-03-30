

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    record_ids = fields.One2many(
        comodel_name='education.record',
        inverse_name='student_id',
        string='Academic Records')
    student = fields.Boolean(
        string='Student')
