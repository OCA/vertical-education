from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpMediaQueue(models.Model):
    _name = 'op.media.queue'
    _inherit = 'mail.thread'
    _rec_name = 'user_id'
    _description = 'Media Queue Request'
    name = fields.Char('Sequence No', readonly=True, copy=False, default='/')
    partner_id = fields.Many2one('res.partner', 'Student/Faculty')
    media_id = fields.Many2one('op.media', required=True, tracking=True)
    date_from = fields.Date('From Date', required=True, default=fields.Date.today())
    date_to = fields.Date('To Date', required=True)
    user_id = fields.Many2one('res.users', readonly=True, default=lambda self: self.env.uid)
    state = fields.Selection([('request', 'Request'), ('accept', 'Accepted'), ('reject', 'Rejected')], 'Status', copy=False, default='request', tracking=True)
    active = fields.Boolean(default=True)

    @api.onchange('user_id')
    def onchange_user(self):
        self.partner_id = self.user_id.partner_id.id

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        if self.date_from > self.date_to:
            raise ValidationError(_('To Date cannot be set before From Date.'))

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not create             Media Queue Requests!'))
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('op.media.queue') or '/'
        return super().create(vals_list)

    def write(self, vals):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not edit             Media Queue Requests!'))
        return super().write(vals)

    def do_reject(self):
        self.state = 'reject'

    def do_accept(self):
        self.state = 'accept'

    def do_request_again(self):
        self.state = 'request'