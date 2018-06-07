# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class WizardInvoicingMethod(models.TransientModel):
    _name = 'wizard.invoicing.method'
    _inherit = 'invoicing.method.plan'

    # invoicing_method_id = fields.Many2one(
    #     comodel_name='invoicing.method',
    #     string='Invoicing Method')

    amount = fields.Float(
        string='invoicing Amount')

    # @api.multi
    # def get_course_invoicing_lines(self):
    #     self.ensure_one()
    #     course_id = self.env.context.get('active_id')
    #     course = self.env['education.course'].browse(course_id)
    #     course.invoicing_method_id = self.invoicing_method_id
    #     course.invoicing_amount = self.amount
    #     for line in course.invoicing_line_ids:
    #         line.unlink()
    #     course.compute_invoicing_method()
    #
    # @api.multi
    # def get_group_invoicing_lines(self):
    #     self.ensure_one()
    #     group_id = self.env.context.get('active_id')
    #     group = self.env['education.group'].browse(group_id)
    #     group.invoicing_method_id = self.invoicing_method_id
    #     group.invoicing_amount = self.amount
    #     for line in group.invoicing_line_ids:
    #         line.unlink()
    #     group.compute_invoicing_method()

    @api.multi
    def get_education_enrollment_invoicing_lines(self):
        self.ensure_one()
        enrollment_id = self.env.context.get('active_id')
        enrollment = self.env[
            'education.enrollment'].browse(enrollment_id)
        enrollment.invoicing_method_id = self.invoicing_method_id.id
        enrollment.invoicing_amount = self.amount
        for line in enrollment.invoicing_line_ids:
            line.unlink()
        enrollment.compute_invoicing_method()
