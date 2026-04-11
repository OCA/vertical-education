import time
from logging import info
from .test_assignment_common import TestAssignmentCommon

class TestAssignment(TestAssignmentCommon):

    def setUp(self):
        super().setUp()

    def test_case_assignment(self):
        assignment = self.op_assignment.search([])
        if not assignment:
            raise AssertionError('Error in data, please check for reference Assignment')
        info('Details of Meeting')
        for record in assignment:
            info(f'      Name : {record.name}')
            info(f'      Course : {record.course_id.id}')
            info(f'      Batch : {record.batch_id.id}')
            info(f'      Subject : {record.subject_id.id}')
            info(f'      Faculty : {record.faculty_id.id}')
            info(f'      Assignment Type : {record.assignment_type.id}')
            info(f'      Marks : {record.marks}')
            info(f'      Description : {record.description}')
            info(f'      State : {record.state}')
            info(f'      Issued_date : {record.issued_date}')
            info(f'      Submission_date : {record.submission_date}')
            info(f'      Allocation Ids : {record.allocation_ids.ids}')
            info(f'      Assignments : {record.assignment_sub_line}')
            info(f'      Reviewer : {record.reviewer.id}')
            record.onchange_course()
            record.act_publish()
            record.act_finish()
            record.act_cancel()
            record.act_set_to_draft()

class TestAssignmentSubline(TestAssignmentCommon):

    def setUp(self):
        super().setUp()

    def test_case_assignment_subline(self):
        assignment_subline = self.op_assignment_subline.search([])
        assignment = self.env['op.assignment'].create({'name': 'LRTP - 001 - Asg - 009', 'state': 'draft', 'marks': 50, 'assignment_type': self.env.ref('openeducat_assignment.op_assignment_1').id, 'issued_date': time.strftime('%Y-%m-01'), 'course_id': self.env.ref('openeducat_core.op_course_4').id, 'batch_id': self.env.ref('openeducat_core.op_batch_3').id, 'subject_id': self.env.ref('openeducat_core.op_subject_10').id, 'faculty_id': self.env.ref('openeducat_core.op_faculty_2').id, 'submission_date': time.strftime('%Y-%m-01'), 'allocation_ids': self.env.ref('openeducat_core.op_student_9'), 'description': 'Please answer the following questions briefly: - 1. What are the different types of land'})
        assignment_subline1 = self.op_assignment_subline.create({'assignment_id': assignment.id, 'state': 'draft', 'student_id': self.env.ref('openeducat_core.op_student_9').id, 'description': 'The answers of the questions are placed here'})
        assignment_subline1.unlink()
        for record in assignment_subline:
            info(f'      Assignment Name : {record.assignment_id.id}')
            info(f'      Student : {record.student_id.id}')
            info(f'      Description : {record.description}')
            info(f'      State : {record.state}')
            info(f'      submission_date : {record.submission_date}')
            info(f'      Marks : {record.marks}')
            info(f'      Note : {record.note}')
            info(f'      User : {record.user_id.id}')
            info(f'      Faculty : {record.faculty_user_id.id}')
            info(f'      Check User Boolean : {record.user_boolean}')
            record.act_draft()
            record.act_submit()
            record.act_accept()
            record.act_change_req()
            record.act_reject()