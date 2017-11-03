# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


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
