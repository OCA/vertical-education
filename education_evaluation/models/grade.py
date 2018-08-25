# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class EducationGrade(models.Model):
    _name = 'education.grade'
    _order = 'end desc'

    name = fields.Char(
        string='name')
    start = fields.Float(
        string='From')
    end = fields.Float(
        string='To')
    grading_id = fields.Many2one(
        comodel_name='education.grading.scale',
        string='Grade')
