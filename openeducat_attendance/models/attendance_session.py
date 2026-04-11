from odoo import fields, models

class OpSession(models.Model):
    _inherit = 'op.session'
    attendance_sheet = fields.One2many('op.attendance.sheet', 'session_id', string='Session')

    def get_attendance(self, context=None):
        sheet = self.env['op.attendance.sheet'].search([('session_id', '=', self.id)])
        register = self.env['op.attendance.register'].search([('course_id', '=', self.course_id.id), ('batch_id', '=', self.batch_id.id)])
        if self.id == sheet.session_id.id:
            if len(sheet) <= 1:
                view_id = (self.env.ref('openeducat_attendance.view_op_attendance_sheet_form').id,)
                return {'name': 'Attendance Sheet', 'view_type': 'form', 'view_mode': 'form', 'views': [(view_id, 'form')], 'res_model': 'op.attendance.sheet', 'view_id': view_id, 'type': 'ir.actions.act_window', 'target': 'current', 'res_id': sheet.id, 'context': {'default_session_id': self.id, 'default_register_id': [rec.id for rec in register]}, 'domain': [('session_id', '=', sheet.session_id.id)]}
            action = self.env.ref('openeducat_attendance.act_open_op_attendance_sheet_view').read()[0]
            action['domain'] = [('session_id', '=', self.id)]
            action['context'] = {'default_session_id': self.id, 'default_register_id': [rec.id for rec in register]}
            return action
        else:
            view_id = (self.env.ref('openeducat_attendance.view_op_attendance_sheet_form').id,)
            return {'name': 'Attendance Sheet', 'view_type': 'form', 'view_mode': 'list', 'views': [(view_id, 'form')], 'res_model': 'op.attendance.sheet', 'view_id': False, 'type': 'ir.actions.act_window', 'target': 'current', 'context': {'default_session_id': self.id, 'default_register_id': [rec.id for rec in register]}, 'domain': [('session_id', '=', self.id)]}