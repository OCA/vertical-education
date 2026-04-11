import time
from odoo import api, fields, models

class ReportMarksheetReport(models.AbstractModel):
    _name = 'report.openeducat_exam.report_marksheet_report'
    _description = 'Exam Marksheet Report'

    def get_objects(self, objects):
        obj = []
        for data in objects:
            obj.extend(data)
        return obj

    def get_lines(self, obj):
        lines = []
        for line in obj.result_line:
            lines.extend(line)
        return lines

    def get_date(self, date):
        date1 = fields.Date.to_date(date)
        return str(date1.month) + ' / ' + str(date1.year)

    def get_total(self, result_line):
        total = [x.exam_id.total_marks for x in result_line]
        return sum(total)

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['op.marksheet.line'].browse(docids)
        docargs = {'doc_model': 'op.marksheet.line', 'docs': docs, 'time': time, 'get_objects': self.get_objects, 'get_lines': self.get_lines, 'get_date': self.get_date, 'get_total': self.get_total}
        return docargs