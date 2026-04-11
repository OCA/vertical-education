from logging import info
from .test_classroom_common import TestClassroomCommon

class TestClassroom(TestClassroomCommon):

    def setUp(self):
        super().setUp()

    def test_case_classroom_1(self):
        classroom = self.op_classroom.search([])
        if not classroom:
            raise AssertionError('Error in data, please check for reference Classroom')
        for record in classroom:
            info(f'      Class Name: {record.name}')
            info(f'      Code : {record.code}')
            info(f'      Course Name : {record.course_id.name}')
            info(f'      Capacity : {record.capacity}')
            for rec in record.facilities:
                info(f'      facilities : {rec.facility_id.name}')
            for rec1 in record.asset_line:
                info(f'      asset_line : {rec1.product_id.name}')
            record.onchange_course()

class TestAsset(TestClassroomCommon):

    def setUp(self):
        super().setUp()

    def test_case_1_asset(self):
        product = self.env['product.product'].create({'default_code': 'FIFO', 'name': 'Chairs', 'categ_id': self.env.ref('product.product_category_1').id, 'list_price': 100.0, 'standard_price': 70.0, 'uom_id': self.env.ref('uom.product_uom_kgm').id, 'uom_po_id': self.env.ref('uom.product_uom_kgm').id, 'description': 'FIFO Ice Cream'})
        assets = self.op_asset.create({'asset_id': self.env.ref('openeducat_classroom.op_classroom_1').id, 'product_id': product.id, 'code': 1, 'product_uom_qty': 11})
        for record in assets:
            info(f'      Asset Name: {record.asset_id.name}')
            info(f'      Product Name : {record.product_id.name}')
            info(f'      Product Quantity : {record.product_uom_qty}')