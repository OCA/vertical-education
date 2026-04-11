from odoo.tests import common

class TestAttendanceCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_attendance_register = self.env['op.attendance.register']
        self.op_attendance_sheet = self.env['op.attendance.sheet']
        self.op_attendance_line = self.env['op.attendance.line']
        self.op_attendance_wizard = self.env['student.attendance']