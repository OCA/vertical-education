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

    def action_view_partner_invoices(self):
        action = self.env.ref('account.action_invoice_refund_out_tree')
        result = action.read()[0]
        result['domain'] = [('partner_id', '=', self.partner_id.id)]
        return result

    def schedule_meeting(self):
        partner_ids = self.ids
        partner_ids.append(self.env.user.partner_id.id)
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        action['context'] = {
            'search_default_partner_ids': self._context['partner_name'],
            'default_partner_ids': partner_ids,
        }
        return action
