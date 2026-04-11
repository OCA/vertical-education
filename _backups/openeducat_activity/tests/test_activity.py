from logging import info
from .test_activity_common import TestActivityCommon

class TestActivity(TestActivityCommon):

    def setUp(self):
        super().setUp()

    def test_case_activity_1(self):
        activity = self.op_activity.search([])
        if not activity:
            raise AssertionError('Error in data, please check for reference ')
        info('Details of Activity')
        for record in activity:
            info(f'      Student : {record.student_id.name}')
            info(f'      Faculty : {record.faculty_id.name}')
            info(f'      Activity Type : {record.type_id.name}')
            info(f'      Description : {record.description}')
            info(f'      Date : {record.date}')

class TestActivityType(TestActivityCommon):

    def setUp(self):
        super().setUp()

    def test_case_1_activity_type(self):
        activity_type = self.op_activity_type.search([])
        if not activity_type:
            raise AssertionError('Error in data, please check for Activity type')
        info('Details of achievement_type')
        for category in activity_type:
            info(f'      Activity : {category.name}')

class TestStudentMigrateWizard(TestActivityCommon):

    def setUp(self):
        super().setUp()

    def test_case_1_student_migrate_wizard(self):
        student_migrate = self.op_student_migrate_wizard.create({'course_from_id': self.env.ref('openeducat_core.op_course_2').id, 'course_to_id': self.env.ref('openeducat_core.op_course_3').id, 'batch_id': self.env.ref('openeducat_core.op_batch_2').id, 'student_ids': self.env.ref('openeducat_core.op_student_1')})
        student_migrate1 = self.op_student_migrate_wizard.create({'course_from_id': self.env.ref('openeducat_core.op_course_3').id, 'course_to_id': self.env.ref('openeducat_core.op_course_2').id, 'batch_id': self.env.ref('openeducat_core.op_batch_1').id, 'student_ids': self.env.ref('openeducat_core.op_student_2')})
        student_migrate.student_migrate_forward()
        student_migrate1.student_by_course()