# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationStudent(models.Model):
    _name = "education.student"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    record_ids = fields.One2many(
        'education.record',
        'student_id',
        'Academic Records')

    def open_partner_history(self):
        action = self.env.ref('account.action_invoice_refund_out_tree')
        result = action.read()[0]
        result['domain'] = [('partner_id', '=', self.partner_id.id)]
        return result
