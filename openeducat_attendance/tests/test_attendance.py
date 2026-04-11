import time
from logging import info
from .test_attendance_common import TestAttendanceCommon

class TestAttendanceRegister(TestAttendanceCommon):

    def setUp(self):
        super().setUp()

    def test_case_attendance_register(self):
        register = self.op_attendance_register.search([])
        for record in register:
            info(f'      Attendance Register : {record.name}')
            info(f'      Course : {record.course_id.name}')
            info(f'      Code : {record.code}')

class TestAttendanceSheet(TestAttendanceCommon):

    def setUp(self):
        super().setUp()

    def test_case_attendance_sheet(self):
        sheet = self.op_attendance_sheet.create({'name': 'AS', 'attendance_date': time.strftime('%Y-%m-01'), 'register_id': self.env.ref('openeducat_attendance.op_attendance_register_1').id})
        info('  Details Of Attendance Sheet:.....')
        for record in sheet:
            record.attendance_draft()
            record.attendance_start()
            record.attendance_done()
            record.attendance_cancel()

class TestAttendanceLine(TestAttendanceCommon):

    def setUp(self):
        super().setUp()

    def test_case_attendance_line(self):
        line = self.op_attendance_line.search([])
        info('  Details Of Attendance Lines:.....')
        for record in line:
            info(f'      Attendance Sheet : {record.attendance_id.name}')
            info(f'      Student : {record.student_id.name}')
            info(f'      Register : {record.register_id.name}')
            info(f'      Present : {record.present}')

class TestAttendanceWizard(TestAttendanceCommon):

    def setUp(self):
        super().setUp()

    def test_case_attendance_wizard(self):
        student = self.op_attendance_wizard.create({'from_date': time.strftime('%Y-%m-01'), 'to_date': time.strftime('%Y-%m-01')})
        student.print_report()