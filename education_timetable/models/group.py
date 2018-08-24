# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, _


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

    def open_group_timetable(self):
        return {
            'name': _("Timetables"),
            'view_mode': 'tree,form',
            'res_model': 'education.timetable.line',
            'src_model': 'education.group',
            'type': 'ir.actions.act_window',
            'domain': '[("group_id", "=", active_id)]'
        }
