# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class EducationGradingScale(models.Model):
    _name = 'education.grading.scale'

    name = fields.Char(
        string='name')
    decimals_number = fields.Integer(
        string='Decimals Number')
    grade_ids = fields.One2many(
        comodel_name='education.grade',
        inverse_name='grading_id',
        string='Califications')
