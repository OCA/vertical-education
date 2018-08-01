
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields


class InvoicingMethod(models.Model):
    _name = 'invoicing.method'

    name = fields.Char(
        string='Name')
    line_ids = fields.One2many(
        comodel_name='invoicing.method.line',
        inverse_name='invoicing_method_id',
        string='Lines')

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id.id,
        string='Company')


class InvoicingMethodLine(models.Model):
    _name = 'invoicing.method.line'
    _order = "sequence"

    name = fields.Char(
        string='name')

    invoicing_method_id = fields.Many2one(
        comodel_name='invoicing.method',
        string='Invoicing Method')
    sequence = fields.Integer(
        string='Sequence',
        default=0)
    type = fields.Selection([
        ('balance', 'Balance'),
        ('percent', 'Percent'),
        ('fixed', 'Fixed Amount')],
        string='Type',
        required=True,
        default='balance')
    amount = fields.Float(
        string='Amount')
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

    @api.onchange('type')
    def _onchange_type(self):
        if self.type == 'balance':
            self.amount = 0

    @api.onchange('quantity')
    def _onchange_quantity(self):
        if self.quantity == 1:
            self.recurring_rule_type = 'none'
