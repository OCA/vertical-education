from odoo.tests import common

class TestTimetableCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_faculty = self.env['op.faculty']
        self.op_session = self.env['op.session']
        self.op_timing = self.env['op.timing']
        self.generate_timetable = self.env['generate.time.table']
        self.wizard_session = self.env['gen.time.table.line']
        self.timetable_report = self.env['time.table.report']