# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import time
from odoo import models, api


class ReportExamStudentLable(models.AbstractModel):
    _name = 'report.education_exam.report_exam_student_lable'

    def format_list(self, temp_list):
        cnt = 1
        temp = {}
        lst = []
        for i in temp_list:
            if cnt <= 3:
                temp.update({str(cnt): i})
                cnt += 1
            else:
                cnt = 1
                lst.append(temp)
                temp = {}
                temp.update({str(cnt): i})
                cnt += 1
        index = len(temp_list) - len(temp_list) % 3
        if len(temp_list) % 3 == 1:
            lst.append({'1': temp_list[index]})
        elif len(temp_list) % 3 == 2:
            lst.append({'1': temp_list[index], '2': temp_list[index + 1]})
        else:
            lst.append(
                {'1': temp_list[-3], '2': temp_list[-2], '3': temp_list[-1]})
        return lst

    def get_student_data(self, docs):
        main_list = []
        for d in docs:
            ret_list = []
            for line in d.exam_session_ids:
                student_ids = self.env['education.student'].search(
                    [('course_detail_ids.course_id', '=', line.course_id.id)],
                    order='id asc')
                temp_list = []
                for student in student_ids:
                    student_course = self.env['education.student.course'].search(
                        [('student_id', '=', student.id),
                         ('course_id', '=', line.course_id.id)])
                    res = {
                        'student': student.name,
                        'course': line.course_id.name,
                        'roll_number': student_course and
                        student_course.roll_number or '',
                    }
                    temp_list.append(res)
                if temp_list:
                    ret_list.append({'course': line.course_id.name,
                                     'line': self.format_list(temp_list)})
            main_list.append(ret_list)
        return main_list

    @api.model
    def render_html(self, docids, data=None):
        docs = self.env['education.exam.res.allocation'].browse(docids)
        docargs = {
            'doc_model': 'education.exam.res.allocation',
            'docs': docs,
            'time': time,
            'get_student_data': self.get_student_data(docs),
        }
        return self.env['report'] \
            .render('education_exam.report_exam_student_lable', docargs)
