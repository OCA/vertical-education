from odoo.tests import TransactionCase

class TestActivityCommon(TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_activity_type = self.env['op.activity.type']
        self.op_activity = self.env['op.activity']
        self.op_student_migrate_wizard = self.env['student.migrate']