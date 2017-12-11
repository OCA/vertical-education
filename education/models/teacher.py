# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EducationTeacher(models.Model):
    _name = "education.teacher"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        ondelete="cascade",
        string='Partner')

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
