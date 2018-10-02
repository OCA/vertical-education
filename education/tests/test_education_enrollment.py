# Copyright (C) 2018-Today: Odoo Community Association (OCA)
# Copyright C)  2018-Today: Pesol (<http://pesol.es>)
# @author: Angel Moya (angel.moya@pesol.es)
# @author: Luis Adan Jimenez (luis.jimenez@pesol.es)
# @author: Adrián Gómez (adrian.gomez@pesol.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestEducationEnrollment(TransactionCase):

    def setUp(self):
        super(TestEducationEnrollment, self).setUp()

        # Group data
        self.group_1 = self.env.ref('education.education_group_1')

        # Enrollment data
        self.enrollment_1 = self.env.ref('education.education_enrollment_1')
        self.enrollment_2 = self.env.ref('education.education_enrollment_2')

    def test_group(self):
        """ Check group flow"""
        self.group_1.action_active()
        self.group_1.action_draft()
        self.group_1.action_active()
        self.group_1.action_done()
        self.group_1.action_cancel()
        self.group_1.action_draft()
        self.group_1.action_active()

    def test_group_unlink(self):
        """ Check group unlink restriction"""
        with self.assertRaises(ValidationError):
            self.group_1.unlink()

    def test_enrollment(self):
        """ Validate enrollment for a full course and check record.
            Validate enrollment on same course for one subject and check
            record for the subjects."""
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
