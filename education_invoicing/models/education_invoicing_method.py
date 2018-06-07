# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields, _


class EducationInvoicingMethod(models.Model):
    _name = 'education.invoicing.method'

    name = fields.Char(
        string='Name',
        compute='_compute_name')
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course')
    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group')
    amount = fields.Float(
        string='Amount')
    enrollment_amount = fields.Float(
        string='Enrollment Amount')
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

    @api.multi
    def _compute_name(self):
        for record in self:
            name = ''
            amount = record.amount
            if record.enrollment_amount:
                name += '%s' % (record.enrollment_amount)
                amount -= record.enrollment_amount
            if record.amount and record.enrollment_amount:
                name += ' + '
            if record.amount:
                if record.quantity and record.quantity > 1:
                    amount = amount / record.quantity
                name += '%s' % (amount)
            if record.quantity and record.quantity > 1:
                name += ' x %s' % (record.quantity)
            record.name = name

    @api.multi
    def compute_invoicing_method(self):
        self.ensure_one()
        amount = self.amount
        invoicing_method_line_data = []
        if self.enrollment_amount:
            line_values = {
                'sequence': 0,
                'name': _('Enrollment'),
                'quantity': 1,
                'subtotal': self.enrollment_amount
            }
            invoicing_method_line_data.append((0, 0, line_values))
            amount -= self.enrollment_amount
        line_values = {
            'sequence': 10,
            'name': _('Fee'),
            'quantity': self.quantity,
            'subtotal': amount / self.quantity,
            'recurring_rule_type': self.recurring_rule_type,
            'recurring_interval': self.recurring_interval,
        }
        invoicing_method_line_data.append((0, 0, line_values))
        return invoicing_method_line_data
