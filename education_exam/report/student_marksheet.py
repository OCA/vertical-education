# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from datetime import datetime
import time

from odoo import models, api


class ReportMarksheetReport(models.AbstractModel):
    _name = 'report.education_exam.report_marksheet_report'

    def get_objects(self, objects):
        obj = []
        for object in objects:
            obj.extend(object)
        return obj

    def get_lines(self, obj):
        lines = []
        for line in obj.marksheet_line:
            lines.extend(line)
        return lines

    def get_date(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%d")
        return str(date1.month) + ' / ' + str(date1.year)

    def get_total(self, marksheet_line):
        total = [x.exam_id.total_marks for x in marksheet_line.result_line]
        return sum(total)

    @api.model
    def render_html(self, docids, data=None):
        docs = self.env['education.marksheet.register'].browse(docids)
        docargs = {
            'doc_model': 'education.marksheet.register',
            'docs': docs,
            'time': time,
            'get_objects': self.get_objects,
            'get_lines': self.get_lines,
            'get_date': self.get_date,
            'get_total': self.get_total,
        }
        return self.env['report'] \
            .render('education_exam.report_marksheet_report', docargs)
