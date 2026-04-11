from odoo.tests import TransactionCase

class TestFeesCommon(TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_student_fees = self.env['op.student.fees.details']
        self.op_student = self.env['op.student']
        self.op_fees_wizard = self.env['fees.detail.report.wizard']
        self.op_fees_terms = self.env['op.fees.terms']