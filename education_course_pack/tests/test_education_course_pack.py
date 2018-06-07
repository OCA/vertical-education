# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase
from datetime import datetime


class TestEducationCoursePack(TransactionCase):

    def setUp(self):
        super(TestEducationCoursePack, self).setUp()
        # Create Student
        self.student = self.env.ref('education.education_student_1')

        # Create Course and Pack
        course_ids = []
        self.course_a = self.env.ref('education.education_course_1')
        course_ids.append(course_a.id)
        self.course_b = self.env.ref('education.education_course_2')
        course_ids.append(course_b.id)
        self.course = self.env.ref('education.education_course_5')
        self.course.write({
            'pack': True,
            'course_pack_line_ids': [(6, 0, course_ids)]
        })
        # Create group
        self.group_a = self.env.ref('education.education_group_1')
        self.group_b = self.env.ref('education.education_group_2')

        # Create Subjects

        self.subject_1 = self.env.ref('education.education_subject_1')
        self.subject_2 = self.env.ref('education.education_subject_2')
        self.course_a.write({
            'subject_ids': subject_1
        })
        self.course_b.write({
            'subject_ids': subject_2
        })
        # Create Subject Registration
        self.education_enrollment = self.env[
            'education.enrollment']
        self.education_enrollment.create({
            'student_id': self.student.id,
            'course_id': self.course.id,
        })
        def test_create_pack_lines(self):
            self.education_enrollment.create_pack_lines()

        self.education_enrollment.course_pack_line_ids[0].write({
            'group_id': self.group_a
        })
        self.education_enrollment.course_pack_line_ids[1].write({
            'group_id': self.group_b
        })
        # Create Education Student Course
        self.education_record = self.env['education.record']
        # self.education_record.create({
        #     'student_id': self.student_id.id,
        #     'course_id': self.course.id,
        #     'group_id': self.group_a
        # })

    def test_get_subjects_pack(self):
        self.education_enrollment.get_subjects_pack()

    def test_do_toggle_approve(self):
        self.education_enrollment.do_toggle_approve()
