import time
from odoo import _, fields, models
from odoo.exceptions import ValidationError

class AdmissionAnalysis(models.TransientModel):
    """Admission Analysis Wizard"""
    _name = 'admission.analysis'
    _description = 'Admission Analysis Wizard'
    course_id = fields.Many2one('op.course', required=True)
    start_date = fields.Date(default=time.strftime('%Y-%m-01'))
    end_date = fields.Date(required=True)

    def print_report(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if start_date > end_date:
            raise ValidationError(_('End Date cannot be set before Start Date.'))
        else:
            data = self.read(['course_id', 'start_date', 'end_date'])[0]
            report = self.env.ref('openeducat_admission.action_report_report_admission_analysis')
            return report.report_action(self, data=data)