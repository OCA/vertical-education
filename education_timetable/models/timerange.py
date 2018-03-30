
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class EducationTimerange(models.Model):
    _name = 'education.timerange'

    name = fields.Char(
        string='Name')

    start_time = fields.Float(
        string='Start time')
    end_time = fields.Float(
        string='End time')
