import time
from odoo import api, models

class ReportMediaBarcode(models.AbstractModel):
    _name = 'report.openeducat_library.report_media_barcode'
    _description = 'Media Barcode Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['op.media'].browse(docids)
        docargs = {'doc_model': 'op.media', 'docs': docs, 'time': time}
        return docargs