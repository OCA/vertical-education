from odoo import models

class OpStudent(models.Model):
    _inherit = 'op.student'

    def get_attendance(self):
        action = self.env.ref('openeducat_attendance.act_open_op_attendance_line_view').sudo().read()[0]
        action['domain'] = [('student_id', 'in', self.ids)]
        return action