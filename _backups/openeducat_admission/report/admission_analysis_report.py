import time
from odoo import api, models

class ReportAdmissionAnalysis(models.AbstractModel):
    _name = 'report.openeducat_admission.report_admission_analysis'
    _description = 'Admission Analysis Report'

    def get_total_student(self, data):
        student_search = self.env['op.admission'].search_count([('state', '=', 'done'), ('course_id', '=', data['course_id'][0]), ('admission_date', '>=', data['start_date']), ('admission_date', '<=', data['end_date'])])
        return student_search

    def get_data(self, data):
        lst = []
        student_search = self.env['op.admission'].search([('state', '=', 'done'), ('course_id', '=', data['course_id'][0]), ('admission_date', '>=', data['start_date']), ('admission_date', '<=', data['end_date'])], order='admission_date desc')
        res = {}
        total_student = 0
        for student in student_search:
            total_student += 1
            res = {'name': student.name, 'application_no': student.application_number}
            lst.append(res)
        return lst

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        docargs = {'doc_ids': self.ids, 'doc_model': model, 'docs': docs, 'time': time, 'data': data, 'start_date': data['start_date'], 'end_date': data['end_date'], 'get_total_student': self.get_total_student(data), 'get_data': self.get_data(data)}
        return docargs