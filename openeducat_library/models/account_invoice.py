from odoo import models

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def action_invoice_paid(self):
        paid_invoice = super().action_invoice_paid()
        if self:
            for record in self:
                movement = self.env['op.media.movement'].sudo().search([('invoice_id', '=', record.id)])
                if movement and movement.invoice_id.state == 'paid':
                    movement.state = 'return_done'
        return paid_invoice