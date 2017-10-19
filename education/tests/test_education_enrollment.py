# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp.tests.common import TransactionCase
import odoo


class TestEducationEnrollment(TransactionCase):

    def setUp(self):
        super(TestEducationEnrollment, self).setUp()

        # Enrollment data
        student_id = self.env.ref('education.education_student_1')
        course_id = self.env.ref('education.education_course_1')
        group_id = self.env.ref('education.education_group_1')
        enrollment_obj = self.env['education.enrollment']

        # Create enrollment
        self.enrollment_id = enrollment_obj.create({
            'student_id': student_id.id,
            'course_id': course_id.id,
            'group_id': group_id.id
        })

        # Get subject function
    def test_get_subjects(self):
        self.enrollment_id.get_subjects()

        # submitt enrollment
    def test_do_toggle_submitted(self):
        self.enrollment_id.do_toggle_submitted()

        # approve enrollment
    def test_do_toggle_approve(self):
        self.enrollment_id.do_toggle_approve()

        # reset draft enrollment
    def test_action_reset_draft(self):
        self.enrollment_id.action_reset_draft()

        # cancell enrollment
    def test_cancelled_enrollment(self):
        self.enrollment_id.cancelled_enrollment()
