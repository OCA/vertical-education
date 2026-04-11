from .test_facility_common import TestFacilityCommon

class TestFacilityLine(TestFacilityCommon):

    def setUp(self):
        super().setUp()

    def test_case_facility_line(self):
        types = self.op_facility_line.create({'facility_id': self.env.ref('openeducat_facility.op_facility_1').id, 'quantity': '1.0'})
        for facility in types:
            facility.check_quantity()