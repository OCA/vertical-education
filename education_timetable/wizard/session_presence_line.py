# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class EducationSessionPresenceLine(models.TransientModel):
    _name = 'education.session.presence.line'

    presence_id = fields.Many2one(
        comodel_name='education.session.presence',
        string='Session Presence')

    student_id = fields.Many2one(
        comodel_name='res.partner',
        string='Student')

    lack = fields.Boolean(
        string='Lack',
    )

    notes = fields.Char(
        string='Notes',
    )
