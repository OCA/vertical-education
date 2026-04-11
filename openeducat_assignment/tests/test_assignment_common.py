from odoo.tests import TransactionCase

class TestAssignmentCommon(TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_assignment = self.env['op.assignment']
        self.op_assignment_subline = self.env['op.assignment.sub.line']