from odoo.tests import common

class TestFacilityCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_facility_line = self.env['op.facility.line']