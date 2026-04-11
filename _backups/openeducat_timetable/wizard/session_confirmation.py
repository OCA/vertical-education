from odoo import models

class SessionConfirmation(models.TransientModel):
    _name = 'session.confirmation'
    _description = 'Wizard for Multiple Session Confirmation'

    def state_confirmation(self):
        active_ids = self.env.context['active_ids']
        lines = self.env['op.session'].search([('id', 'in', active_ids), ('state', '=', 'draft')])
        for line in lines:
            line.lecture_confirm()