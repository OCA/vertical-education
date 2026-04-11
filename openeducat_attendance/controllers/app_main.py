from odoo import fields, http
from odoo.http import request

class OpAttendanceController(http.Controller):

    @http.route(['/openeducat-attendance/take-attendance'], type='json', auth='none', methods=['POST'], csrf=False)
    def create_attendance_lines(self, **post):
        sheet_id = post.get('attendance_sheet_id', False)
        if sheet_id:
            attend_lines = request.env['op.attendance.line'].sudo()
            sheet = request.env['op.attendance.sheet'].sudo().browse([sheet_id])
            all_student_search = request.env['op.student'].sudo().search([('course_detail_ids.course_id', '=', sheet.register_id.course_id.id), ('course_detail_ids.batch_id', '=', sheet.register_id.batch_id.id)])
            attendance_lines = attend_lines.search([('attendance_id', '=', sheet.id)])
            a = [x.id for x in all_student_search]
            b = [x.student_id.id for x in attendance_lines]
            remaining_students = set(a).difference(b)
            for student in remaining_students:
                attend_lines.create({'attendance_id': sheet.id, 'student_id': student, 'attendance_date': fields.Date.today(), 'present': True})
        return True