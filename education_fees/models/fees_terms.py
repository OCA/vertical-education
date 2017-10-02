# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, api, fields, exceptions, _


class EducationFeesTermsLine(models.Model):
    _name = 'education.fees.terms.line'

    due_days = fields.Integer('Due Days')
    value = fields.Float('Value (%)')
    fees_id = fields.Many2one('education.fees.terms', 'Fees')


class EducationFeesTerms(models.Model):
    _name = 'education.fees.terms'

    name = fields.Char('Fees Terms', required=True)
    active = fields.Boolean('Active', default=True)
    note = fields.Text('Description')
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    no_days = fields.Integer('No of Days')
    day_type = fields.Selection([('before', 'Before'), ('after', 'After')],
                                'Type')
    line_ids = fields.One2many('education.fees.terms.line', 'fees_id', 'Terms')

    @api.model
    def create(self, vals):
        res = super(EducationFeesTerms, self).create(vals)
        if not res.line_ids:
            raise exceptions.AccessError(_("Fees Terms must be Required!"))
        total = 0.0
        for line in res.line_ids:
            if line.value:
                total += line.value
        if total != 100.0:
            raise exceptions.AccessError(_("Fees terms must be divided \
            as such sum up in 100%"))
        return res
