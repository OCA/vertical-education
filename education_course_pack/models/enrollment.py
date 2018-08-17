# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields


class EducationEnrollment(models.Model):
    _inherit = 'education.enrollment'

    pack = fields.Boolean(
        string='Pack',
        related='course_id.pack')
    parent_enrollment_id = fields.Many2one(
        comodel_name='education.enrollment',
        string='Parent Enrollment')
    pack_enrollment_ids = fields.One2many(
        comodel_name='education.enrollment',
        inverse_name='parent_enrollment_id',
        string='Pack enrollment')
    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group',
        required=False)

    state = fields.Selection(selection_add=[('in_process', "In Process")])

    @api.multi
    def action_done(self):
        if self.pack:
            super(EducationEnrollment, self).action_done()
            self.create_pack_lines()
            self.state = 'in_process'
        else:
            super(EducationEnrollment, self).action_done()

    @api.multi
    def create_pack_lines(self):
        self.ensure_one()
        if not self.pack:
            # TODO: warning
            return True
        line_values = []
        for course in self.course_id.course_pack_line_ids:
            data = {
                'student_id': self.student_id.id,
                # 'partner_id': self.partner_id.id,
                'course_id': course.id,
                'subject_ids': [(6, 0, course.subject_ids.ids)]
            }
            line_values.append((0, 0, data))
        self.write({'pack_enrollment_ids': line_values})

    @api.multi
    def get_record_values(self):
        if self.pack:
            return {
                # 'partner_id': self.partner_id.id,
                'student_id': self.student_id.id,
                'course_id': self.course_id.id,
            }
        else:
            values = super(EducationEnrollment, self).get_record_values()
            if self.parent_enrollment_id:
                values.update({
                    'parent_record_id': self.parent_enrollment_id.record_id.id
                })
            return values

    @api.multi
    def set_done(self):
        if not self.pack:
            super(EducationEnrollment, self).set_done()

    @api.onchange('course_id')
    def _onchange_course(self):
        self.pack = self.course_id.pack

    # @api.onchange('course_id')
    # def _onchange_course(self):
    #     if self.course_id.pack:
    #         self.invoicing_amount = self.course_id.total
    #         self.invoicing_method_line_ids = [
    #             (0, 0, {
    #                 'name': i.name,
    #                 'sequence': i.sequence,
    #                 'quantity': i.quantity,
    #                 'subtotal': i.subtotal,
    #                 'total': i.total,
    #                 'recurring_rule_type': i.recurring_rule_type,
    #                 'recurring_interval': i.recurring_interval,
    #             }) for i in self.group_id.invoicing_method_ids
    #         ]
