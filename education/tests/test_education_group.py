# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase
import odoo


class TestEducationGroup(TransactionCase):

    def setUp(self):
        super(TestEducationGroup, self).setUp()

        # group data
        self.group_id = self.env.ref('education.education_group_1')


        # Set active
    def test_set_active(self):
        self.group_id.set_active()

        # create group
    def test_create(self):
        group_obj = self.env['education.group']
        self.group = group_obj.create({
            'name': 'group_test',
            'course_id': self.env.ref('education.education_course_1').id
        })
