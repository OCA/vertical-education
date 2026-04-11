from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpMarksheetRegister(models.Model):
    _name = 'op.marksheet.register'
    _inherit = ['mail.thread']
    _description = 'Marksheet Register'
    exam_session_id = fields.Many2one('op.exam.session', required=True, tracking=True)
    marksheet_line = fields.One2many('op.marksheet.line', 'marksheet_reg_id', 'Marksheets')
    generated_date = fields.Date(required=True, default=fields.Date.today(), tracking=True)
    generated_by = fields.Many2one('res.users', default=lambda self: self.env.uid, required=True, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('cancelled', 'Cancelled')], 'Status', default='draft', required=True, tracking=True)
    total_pass = fields.Integer(compute='_compute_total_pass', tracking=True, store=True)
    total_failed = fields.Integer('Total Fail', compute='_compute_total_failed', tracking=True, store=True)
    name = fields.Char('Marksheet Register', size=256, required=True, tracking=True)
    result_template_id = fields.Many2one('op.result.template', required=True, tracking=True)
    active = fields.Boolean(default=True)

    @api.constrains('total_pass', 'total_failed')
    def _check_marks(self):
        for res in self:
            if res.total_pass < 0.0 or res.total_failed < 0.0:
                raise ValidationError(_('Enter proper pass or fail!'))

    @api.depends('marksheet_line.status')
    def _compute_total_pass(self):
        for record in self:
            count = 0
            for marksheet in record.marksheet_line:
                if marksheet.status == 'pass':
                    count += 1
            record.total_pass = count

    @api.depends('marksheet_line.status')
    def _compute_total_failed(self):
        for record in self:
            count = 0
            for marksheet in record.marksheet_line:
                if marksheet.status == 'fail':
                    count += 1
            record.total_failed = count

    def action_validate(self):
        self.state = 'validated'

    def act_cancel(self):
        self.state = 'cancelled'

    def act_draft(self):
        self.state = 'draft'