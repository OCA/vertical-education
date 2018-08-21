
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestEducationEnrollment(TransactionCase):

    def setUp(self):
        super(TestEducationEnrollment, self).setUp()

        # Enrollment data
        self.enrollment_1 = self.env.ref('education.education_enrollment_1')
        self.enrollment_2 = self.env.ref('education.education_enrollment_2')

    def test_enrollment(self):
        self.enrollment_1.action_done()
        record_subject_ids = \
            self.enrollment_1.record_id.record_subject_ids.mapped('subject_id')
        course_subject_ids = \
            self.enrollment_1.subject_ids

        self.assertEquals(record_subject_ids, course_subject_ids)

        self.enrollment_2.action_done()
        record = self.enrollment_2.record_id

        self.assertEquals(
            record, self.enrollment_1.record_id)

        subjects_enrolled = self.enrollment_2.subject_ids
        record_subject = record.record_subject_ids.filtered(
            lambda s: s.subject_id in subjects_enrolled)
        self.assertEquals(
            record_subject.record_subject_group_ids.mapped('enrollment_id'),
            self.enrollment_1 + self.enrollment_2)
