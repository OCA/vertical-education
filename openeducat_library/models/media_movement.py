from datetime import datetime, timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

def days_between(to_date, from_date):
    to_date = fields.Datetime.from_string(to_date)
    from_date = fields.Datetime.from_string(from_date)
    return abs((from_date - to_date).days)

class OpMediaMovement(models.Model):
    _name = 'op.media.movement'
    _inherit = 'mail.thread'
    _description = 'Media Movement'
    _rec_name = 'media_id'
    _order = 'id DESC'
    media_id = fields.Many2one('op.media', required=True)
    media_unit_id = fields.Many2one('op.media.unit', required=True, tracking=True, domain=[('state', '=', 'available')])
    type = fields.Selection([('student', 'Student'), ('faculty', 'Faculty')], 'Student/Faculty', required=True)
    student_id = fields.Many2one('op.student')
    faculty_id = fields.Many2one('op.faculty')
    library_card_id = fields.Many2one('op.library.card', required=True, tracking=True)
    issued_date = fields.Date(tracking=True, required=True, default=fields.Date.today())
    return_date = fields.Date('Due Date', required=True)
    actual_return_date = fields.Date()
    penalty = fields.Float()
    partner_id = fields.Many2one('res.partner', 'Person', tracking=True)
    reserver_name = fields.Char('Person Name', size=256)
    state = fields.Selection([('available', 'Available'), ('reserve', 'Reserved'), ('issue', 'Issued'), ('lost', 'Lost'), ('return', 'Returned'), ('return_done', 'Returned Done')], 'Status', default='available', tracking=True)
    media_type_id = fields.Many2one(related='media_id.media_type_id', store=True)
    user_id = fields.Many2one('res.users', string='Users')
    invoice_id = fields.Many2one('account.move', readonly=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)

    def get_diff_day(self):
        for media_mov_id in self:
            today_date = datetime.strptime(str(fields.Date.today()), '%Y-%m-%d')
            return_date = datetime.strptime(str(media_mov_id.return_date), '%Y-%m-%d')
            diff = today_date - return_date
            return abs(diff.days)

    @api.constrains('issued_date', 'return_date')
    def _check_date(self):
        for record in self:
            if record.issued_date > record.return_date:
                raise ValidationError(_('Return Date cannot be set before Issued Date.'))

    @api.constrains('issued_date', 'actual_return_date')
    def check_actual_return_date(self):
        for record in self:
            if record.actual_return_date:
                if record.issued_date > record.actual_return_date:
                    raise ValidationError(_('Actual Return Date cannot be set before Issued Date'))

    @api.onchange('media_unit_id')
    def onchange_media_unit_id(self):
        self.state = self.media_unit_id.state
        self.media_id = self.media_unit_id.media_id

    @api.onchange('library_card_id')
    def onchange_library_card_id(self):
        self.type = self.library_card_id.type
        self.return_date = self.issued_date + timedelta(days=self.library_card_id.library_card_type_id.duration)
        if self.type == 'student':
            self.student_id = self.library_card_id.student_id.id or False
            self.partner_id = self.student_id.partner_id.id or False
            self.user_id = self.student_id.user_id.id or False
        else:
            self.faculty_id = self.library_card_id.faculty_id.id or False
            self.partner_id = self.faculty_id.partner_id.id or False
            self.user_id = self.faculty_id.user_id.id or False

    @api.onchange('issued_date')
    def onchange_issued_date(self):
        self.return_date = self.issued_date + timedelta(days=self.library_card_id.library_card_type_id.duration or 1)

    def issue_media(self):
        """function to issue media"""
        for record in self:
            if record.media_unit_id.state and record.media_unit_id.state == 'available':
                record.media_unit_id.state = 'issue'
                record.state = 'issue'

    def return_media(self, return_date):
        for record in self:
            if not return_date:
                return_date = fields.Date.today()
            record.actual_return_date = return_date
            record.calculate_penalty()
            if record.penalty > 0.0:
                record.state = 'return'
            else:
                record.state = 'return_done'
            record.media_unit_id.state = 'available'

    def calculate_penalty(self):
        for record in self:
            penalty_amt = 0
            penalty_days = 0
            standard_diff = days_between(record.return_date, record.issued_date)
            actual_diff = days_between(record.actual_return_date, record.issued_date)
            x = record.library_card_id.library_card_type_id
            if record.library_card_id and x:
                penalty_days = actual_diff > standard_diff and actual_diff - standard_diff or penalty_days
                penalty_amt = penalty_days * x.penalty_amt_per_day
            record.write({'penalty': penalty_amt})

    def create_penalty_invoice(self):
        for rec in self:
            account_id = False
            product = self.env.ref('openeducat_library.op_product_7')
            if product.id:
                account_id = product.property_account_income_id.id
            if not account_id:
                account_id = product.categ_id.property_account_income_categ_id.id
            if not account_id:
                raise UserError(_('There is no income account defined for this                     product: "%s". You may have to install a chart of                     account from Accounting app, settings                     menu.') % (product.name,))
            invoice = self.env['account.move'].create({'partner_id': rec.student_id.partner_id.id, 'move_type': 'out_invoice', 'invoice_date': fields.Date.today()})
            line_values = {'name': product.name, 'account_id': account_id, 'price_unit': rec.penalty, 'quantity': 1.0, 'discount': 0.0, 'product_uom_id': product.uom_id.id, 'product_id': product.id}
            invoice.write({'invoice_line_ids': [(0, 0, line_values)]})
            invoice._compute_tax_totals()
            self.invoice_id = invoice.id