
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestEducationEnrollment(TransactionCase):

    def setUp(self):
        super(TestEducationEnrollment, self).setUp()

        # Enrollment data
        self.enrollment = self.env.ref('education.education_enrollment_1')

    def test_action_done(self):
        self.enrollment.action_done()
        record_subject_ids = \
            self.enrollment.record_id.record_subject_ids.mapped('subject_id')
        course_subject_ids = \
            self.enrollment.subject_ids

        self.assertEquals(record_subject_ids, course_subject_ids)
