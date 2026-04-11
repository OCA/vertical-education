from odoo.tests import TransactionCase

class TestCoreCommon(TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_batch = self.env['op.batch']
        self.op_faculty = self.env['op.faculty']
        self.op_course = self.env['op.course']
        self.res_company = self.env['res.users']
        self.op_student = self.env['op.student']
        self.hr_emp = self.env['hr.employee']
        self.subject_registration = self.env['op.subject.registration']
        self.op_update = self.env['publisher_warranty.contract']
        self.employ_wizard = self.env['wizard.op.faculty.employee']
        self.faculty_user_wizard = self.env['wizard.op.faculty']
        self.studnet_wizard = self.env['wizard.op.student']