# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class EducationVacation(models.Model):
    _name = 'education.vacation'
    _inherit = 'education.timetable.line'

    name = fields.Char(
        string='Name')

    init_date = fields.Date(
        string='Init Date')

    end_date = fields.Date(
        string='End Date')

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company')
