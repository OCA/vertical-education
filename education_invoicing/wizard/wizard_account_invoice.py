# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WizardAccountInvoice(models.TransientModel):
    _name = 'wizard.account.invoice'

    partial_amount = fields.Float(
        string='Partial Amount')

    @api.multi
    def validate_partial_payment(self):
        invoice_id = self._context.get('active_id')
        invoice = self.env['account.invoice'].browse(invoice_id)
        old_invoice_amount = invoice.amount_total
        if self.partial_amount >= invoice.amount_total or \
                self.partial_amount <= 0:
            raise ValidationError(
                _("The partial amount must be lower than the total invoice amount"))
        else:
            duplicate_invoice = invoice.copy()
            invoice.invoice_line_ids[0].price_unit = self.partial_amount
            duplicate_invoice.invoice_line_ids[
                0].price_unit -= self.partial_amount
            # create new education invoice method line
            enrollment_obj = self.env['education.enrollment'].browse(
                duplicate_invoice.enrollment_id.id)
            enrollment_method_line = self.env[
                'education.enrollment.invoicing.method.line']
            for record in duplicate_invoice.invoice_line_ids:
                lines = enrollment_method_line.create({
                    'name': record.name,
                    'state': 'draft',
                    'enrollment_id': duplicate_invoice.enrollment_id.id,
                    'sequence': 0,
                    'quantity': 1,
                    'subtotal': record.price_unit,
                    'invoiced': False
                })
            lines.invoice_ids = duplicate_invoice
            for record in enrollment_obj.invoicing_line_ids:
                if record.subtotal == old_invoice_amount:
                    record.enrollment_id = False
            invoice.paid_and_validate()
            # enrollment_obj.invoices_generate()
