# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import TransactionCase


class TestEducationCRM(TransactionCase):

    def setUp(self):
        super(TestEducationCRM, self).setUp()
        self.crm = self.env.ref('crm.crm_case_13')

    def test_create_student(self):
        self.crm.create_student()
