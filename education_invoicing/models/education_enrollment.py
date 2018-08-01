
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.osv import expression
import odoo.addons.decimal_precision as dp


class EducationEnrollment(models.Model):
    _inherit = 'education.enrollment'

    invoices_count = fields.Integer(
        string='Invoices',
        compute='_compute_count_invoices')
    invoice_ids = fields.One2many(
        comodel_name='account.invoice',
        inverse_name='enrollment_id',
        track_visibility='always',
        string='Invoices')
    invoicing_price = fields.Float(
        string='Invoicing Price',
        related='invoicing_method_id.amount')
    invoicing_method_id = fields.Many2one(
        comodel_name='education.invoicing.method',
        string='Invoicing Method')
    invoicing_method_amount = fields.Float(
        string='Invoicing Method Amount',
        compute='_compute_invoicing_method_amount')
    invoicing_amount = fields.Float(
        string='Invoicing Amount',)
    invoicing_line_ids = fields.One2many(
        comodel_name='education.enrollment.invoicing.line',
        inverse_name='enrollment_id',
        string='Invoicing Method line')
    total = fields.Float(
        string='Total',
        store=True,
        compute='_compute_total',)
    date = fields.Date(
        string='Date')
    amount = fields.Float(
        string='Amount')
    enrollment_amount = fields.Float(
        string='Enrollment Amount')
    first_fee_date = fields.Date(
        string='First Fee Date')
    quantity = fields.Integer(
        string='Quantity',
        default=1)
    recurring_rule_type = fields.Selection(
        [('none', 'None'),
         ('daily', 'Day(s)'),
         ('weekly', 'Week(s)'),
         ('monthly', 'Month(s)'),
         ('monthlylastday', 'Month(s) last day'),
         ('yearly', 'Year(s)'),
         ],
        default='none',
        string='Recurrence',
        help="Specify Interval for automatic invoice generation.",
    )
    recurring_interval = fields.Integer(
        default=1,
        string='Repeat Every',
        help="Repeat every (Days/Week/Month/Year)",
    )

    # TODO: account_payment_partner module
    # payment_mode_id = fields.Many2one(
    #     comodel_name='account.payment.mode',
    #     string='Payment Mode')

    @api.onchange('invoicing_method_id')
    def _onchange_invoicing_method_id(self):
        self.enrollment_amount = self.invoicing_method_id.enrollment_amount
        self.amount = self.invoicing_method_id.amount
        self.quantity = self.invoicing_method_id.quantity
        self.recurring_interval = self.invoicing_method_id.recurring_interval
        self.recurring_rule_type = self.invoicing_method_id.recurring_rule_type
        # self.invoicing_line_ids = \
        #     self.invoicing_method_id and \
        #     self.invoicing_method_id.compute_invoicing_method() or False

    @api.multi
    def compute_invoicing_method(self):
        self.ensure_one()
        amount = self.amount
        invoicing_method_line_data = []
        if self.enrollment_amount:
            line_values = {
                'sequence': 0,
                'name': 'enrollment',
                'quantity': 1,
                'subtotal': self.enrollment_amount
            }
            invoicing_method_line_data.append((0, 0, line_values))
            amount -= self.enrollment_amount
        line_values = {
            'sequence': 10,
            'name': 'fee',
            'quantity': self.quantity,
            'subtotal': amount / self.quantity,
            'recurring_rule_type': self.recurring_rule_type,
            'recurring_interval': self.recurring_interval,
        }
        invoicing_method_line_data.append((0, 0, line_values))
        self.invoicing_line_ids = invoicing_method_line_data

    @api.multi
    @api.depends('invoicing_line_ids.total',
                 'invoicing_line_ids.subtotal',
                 'invoicing_line_ids.quantity')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.invoicing_line_ids.mapped(
                lambda l: l.subtotal * l.quantity
            ))

    @api.multi
    def _compute_invoicing_method_amount(self):
        for record in self:
            record.invoicing_method_amount = sum(
                self.invoicing_line_ids.mapped(
                    lambda l: l.subtotal * l.quantity
                ))

    @api.multi
    def invoices_generate(self):
        self.ensure_one()
        # TODO: generate invoices on planned date
        product_obj = self.env['product.product'].search([
            ('name', '=', 'Pagos'),
            ('company_id', '=', self.env.user.company_id.id)
        ])
        if not product_obj:
            product_obj = self.env['product.product'].create({
                'name': 'Pagos',
                'taxes_id': False,
                'supplier_taxes_id': False,
                'type': 'service',
                'company_id': self.env.user.company_id.id
            })
        product_id = product_obj and product_obj[0]
        invoice_obj = self.env['account.invoice']
        account_journal_obj = self.env['account.journal']
        account_journal_id = account_journal_obj.search([
            ('type', 'in', ['sale']),
            ('company_id', '=', self.env.user.company_id.id)
        ], limit=1)
        last_date = False
        date = self.group_id.date_from or fields.Date.today()
        for line in self.invoicing_line_ids.filtered(
                lambda l: l.state == 'none' or l.state == 'draft'):
            line_date = date or line.date
            if line.invoice_ids:
                line.invoice_ids.unlink()
            for a in range(0, line.quantity):
                if a >= 0:
                    if line.recurring_rule_type == 'monthly':
                        last_date = fields.Date.from_string(
                            line_date) + relativedelta(months=a + 1)
                    elif line.recurring_rule_type == 'daily':
                        last_date = fields.Date.from_string(
                            line_date) + relativedelta(days=a + 1)
                    elif line.recurring_rule_type == 'weekly':
                        week_qty = a + 1
                        last_date = fields.Date.from_string(
                            line_date) + relativedelta(days=(week_qty) * 7)
                    if not line.recurring_rule_type:
                        last_date = line_date

                invoice_line_data = {
                    'product_id': product_id.id,
                    'name': line.name,
                    'account_id':
                    account_journal_id.default_debit_account_id.id,
                    'quantity': 1,
                    'price_unit': line.subtotal
                }
                invoice_obj.create({
                    'partner_id': self.student_id.id,
                    'enrollment_id': self.id,
                    'journal_id': account_journal_id.id,
                    'account_id':
                    self.student_id.property_account_receivable_id.id,
                    'date_invoice': last_date,
                    'planned_date': last_date,
                    'method_line_id': line.id,
                    'invoice_line_ids': [(0, 0, invoice_line_data)],
                    'enrollment_invoicing_line_id': line.id,
                })
                line.write({
                    'state': 'draft',
                })

    @api.onchange('group_id')
    def _onchange_group_id(self):
        if not self.group_id:
            return {'domain': {'invoicing_method_id': expression.FALSE_DOMAIN}}
        invoicing_fields_domain = [
            ('id', 'in', self.group_id.invoicing_method_ids.ids)]
        return {'domain': {'invoicing_method_id': invoicing_fields_domain}}

    @api.multi
    def _compute_count_invoices(self):
        for record in self:
            record.invoices_count = self.env['account.invoice'].search_count(
                [('partner_id', '=', record.student_id.id),
                 ('enrollment_id', '=', record.id)])

    @api.multi
    def action_done(self):
        super(EducationEnrollment, self).action_done()
        self.student_id.write({
            'customer': True
        })
        self.compute_invoicing_method()
        self.invoices_generate()

    @api.multi
    def unlink(self):
        for record in self:
            if not record.invoice_ids.filtered(
                    lambda i: i.state in ['paid', 'open']):
                return super(EducationEnrollment, self).unlink()
            else:
                raise ValidationError(
                    _('You can not delete an enrollment with open '
                      'or paid invoices'))


class EducationEnrollmentInvoicingMethodLine(models.Model):
    _name = 'education.enrollment.invoicing.line'
    _order = "sequence"

    name = name = fields.Selection(
        [('enrollment', 'Enrollment'),
         ('fee', 'Fee')],
        string='Type')
    state = fields.Selection(
        [('invoiced', 'Invoiced'),
         ('paid', 'Paid'),
         ('draft', 'Draft'),
         ('none', 'None')],
        string='Status',
        default='none',
        readonly=True)
    enrollment_id = fields.Many2one(
        comodel_name='education.enrollment',
        string='Enrollment')
    sequence = fields.Integer(
        string='Sequence')
    quantity = fields.Integer(
        string='Quantity',
        default=1)
    subtotal = fields.Float(
        string='Subtotal',
        digits=dp.get_precision('Product Price'))
    total = fields.Float(
        string='Total',
        compute='_compute_total')
    recurring_rule_type = fields.Selection(
        [('none', 'None'),
         ('daily', 'Day(s)'),
         ('weekly', 'Week(s)'),
         ('monthly', 'Month(s)'),
         ('monthlylastday', 'Month(s) last day'),
         ('yearly', 'Year(s)')],
        default='monthly',
        string='Recurrence',
        help="Specify Interval for automatic invoice generation.",
    )
    recurring_interval = fields.Integer(
        default=1,
        string='Repeat Every',
        help="Repeat every (Days/Week/Month/Year)",
    )
    date = fields.Datetime(
        string='Invoice Date')

    invoice_ids = fields.One2many(
        comodel_name='account.invoice',
        inverse_name='enrollment_invoicing_line_id',
        string='Invoices')

    invoiced = fields.Boolean(
        string='Invoiced')

    @api.multi
    @api.depends('subtotal', 'quantity')
    def _compute_total(self):
        for record in self:
            record.total = record.subtotal * record.quantity

    @api.multi
    def unlink(self):
        if self.invoice_ids and self.invoiced:
            raise ValidationError(
                _("Once the invoice has been paid, the line can not be deleted"
                  )
            )
        else:
            for line in self.invoice_ids:
                invoice = self.env['account.invoice'].browse(line.id)
                invoice.unlink()
            # self.invoice_id.unlink()
            return super(EducationEnrollmentInvoicingMethodLine, self).unlink()
