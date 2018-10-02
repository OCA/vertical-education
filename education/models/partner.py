# Copyright (C) 2018-Today: Odoo Community Association (OCA)
# Copyright C)  2018-Today: Pesol (<http://pesol.es>)
# @author: Angel Moya (angel.moya@pesol.es)
# @author: Luis Adan Jimenez (luis.jimenez@pesol.es)
# @author: Adrián Gómez (adrian.gomez@pesol.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    teacher = fields.Boolean(
        string='Teacher')
    student = fields.Boolean(
        string='Student')
    record_ids = fields.One2many(
        comodel_name='education.record',
        inverse_name='student_id',
        string='Academic Records')

    def open_student_enrolled_groups(self):
        return {
            'name': _("Academic Groups"),
            'view_mode': 'tree,form',
            'res_model': 'education.group',
            'src_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'domain': '[("enrollment_ids.student_id", "=", active_id)]',
            # 'context': '{"search_default_state": "active"}'
        }

    def open_teacher_active_groups(self):
        return {
            'name': _("Academic Groups"),
            'view_mode': 'tree,form',
            'res_model': 'education.group',
            'src_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'domain': '[("tutor_id", "=", active_id)]',
            'context': '{"search_default_state": "active"}'
        }

    def open_student_enrollments(self):
        return {
            'name': _("Enrollments"),
            'view_mode': 'tree,form',
            'res_model': 'education.enrollment',
            'src_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'domain': '[("student_id", "=", active_id)]'
        }
