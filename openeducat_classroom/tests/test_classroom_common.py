from odoo.tests import common

class TestClassroomCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_classroom = self.env['op.classroom']
        self.op_asset = self.env['op.asset']