# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import http, fields
from odoo.http import request


class OpAttendanceController(http.Controller):

    @http.route(['/education-attendance/take-attendance'], type='json',
                auth='none', methods=['POST'], csrf=False)
    def create_attendance_lines(self, **post):
        sheet_id = post.get('attendance_sheet_id', False)

        if sheet_id:

            sheet = request.env[
                'education.attendance.sheet'].sudo().browse([sheet_id])

            all_student_search = request.env['education.student'].sudo().search(
                [('course_detail_ids.course_id', '=',
                  sheet.register_id.course_id.id),
                 ('course_detail_ids.batch_id', '=',
                  sheet.register_id.batch_id.id)])

            attendance_lines = request.env['education.attendance.line'].sudo().search(
                [('attendance_id', '=', sheet.id)])
            a = [x.id for x in all_student_search]
            b = [x.student_id.id for x in attendance_lines]
            remaining_students = set(a).difference(b)

            for student in remaining_students:
                request.env['education.attendance.line'].sudo().create(
                    {'attendance_id': sheet.id,
                     'student_id': student,
                     'attendance_date': fields.Date.today(),
                     'present': True})
        return True
