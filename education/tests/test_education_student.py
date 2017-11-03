# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase
import odoo


class TestEducationStudent(TransactionCase):

    def setUp(self):
        super(TestEducationStudent, self).setUp()

        # group data
        self.student_id = self.env.ref('education.education_student_1')

        # Open student history
    def test_open_partner_history(self):
        self.student_id.open_partner_history()
