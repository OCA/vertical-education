from odoo.tests import common

class TestLibraryCommon(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.op_library_card_type = self.env['op.library.card.type']
        self.op_library_card = self.env['op.library.card']
        self.op_media = self.env['op.media']
        self.op_media_unit = self.env['op.media.unit']
        self.op_media_movement = self.env['op.media.movement']
        self.op_media_purchase = self.env['op.media.purchase']
        self.op_media_queue = self.env['op.media.queue']
        self.wizard_issue = self.env['issue.media']
        self.reserve_media = self.env['reserve.media']
        self.return_media = self.env['return.media']