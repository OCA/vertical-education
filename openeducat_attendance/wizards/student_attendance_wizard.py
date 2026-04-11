from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class StudentAttendance(models.TransientModel):
    _name = 'student.attendance'
    _description = 'Student Attendance'
    from_date = fields.Date(required=True, default=lambda self: fields.Date.today())
    to_date = fields.Date(required=True, default=lambda self: fields.Date.today())

    @api.constrains('from_date', 'to_date')
    def check_dates(self):
        for record in self:
            from_date = fields.Date.from_string(record.from_date)
            to_date = fields.Date.from_string(record.to_date)
            if to_date < from_date:
                raise ValidationError(_('To Date cannot be set before From Date.'))

    def print_report(self):
        data = self.read(['from_date', 'to_date'])[0]
        data.update({'student_id': self.env.context.get('active_id', False)})
        return self.env.ref('openeducat_attendance.action_report_student_attendance').report_action(self, data=data)