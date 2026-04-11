from logging import info
from .test_fees_common import TestFeesCommon

class TestStudentFees(TestFeesCommon):

    def setUp(self):
        super().setUp()

    def test_case_fees(self):
        fees = self.op_student_fees.search([])
        if not fees:
            raise AssertionError('Error in data, please check for student fees details')
        info('  Details Of Student Fees:.....')
        for record in fees:
            record.action_get_invoice()

class TestStudent(TestFeesCommon):

    def setUp(self):
        super().setUp()

    def test_case_student_fees(self):
        student = self.op_student.search([])
        if not student:
            raise AssertionError('Error in data, please check for student fees invoice details')
        info('  Details Of Student Fees Invoice:.....')
        for record in student:
            record.action_view_invoice()

class TestWizardFees(TestFeesCommon):

    def setUp(self):
        super().setUp()

    def test_case_wizard_fees(self):
        wizard = self.op_fees_wizard.create({'fees_filter': 'student', 'student_id': self.env.ref('openeducat_core.op_student_1').id})
        info('  Details Of Student Fees :.....')
        wizard.print_report()

class TestFeesTerms(TestFeesCommon):

    def setUp(self):
        super().setUp()

    def test_case_fees_terms(self):
        terms = self.op_fees_terms.create({'name': 'Library Fees', 'code': 'LIB_FEE', 'line_ids': [(4, self.env.ref('openeducat_fees.op_fees_term_line_6').id)]})
        info('  Details Of Fees Terms :.....')
        return terms