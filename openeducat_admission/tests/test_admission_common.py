from odoo.tests import TransactionCase

class TestAdmissionCommon(TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_register = self.env['op.admission.register']
        self.op_admission = self.env['op.admission']
        self.wizard_admission = self.env['admission.analysis']