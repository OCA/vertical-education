
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestEducationEvaluation(TransactionCase):

    def setUp(self):
        super(TestEducationEvaluation, self).setUp()

        # Enrollment data
        self.enrollment_3 = self.env.ref('education.education_enrollment_3')
        self.exam_1 = self.env.ref('education.education_exam_1')

    def test_evaluation(self):
        self.enrollment_3.action_done()
        self.assertEquals(self.enrollment_3.grading_id,
                          self.enrollment_3.course_id.grading_id)
        self.assertEquals(self.enrollment_3.record_id.grading_id,
                          self.enrollment_3.course_id.grading_id)
        self.exam_1.set_planned()
        for result in self.exam_1:
            result.score = 6.7
            self.exam_1.set_done()
        for record_subject in self.enrollment_3.record_id.record_subject_ids:
            self.assertEquals(record_subject.weight, 'course_subject_id')
