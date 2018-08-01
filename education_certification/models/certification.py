
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields
from odoo.osv import expression


class EducationCertification(models.Model):
    _name = 'education.certification'

    name = fields.Char(
        string='Name')
    type = fields.Selection(
        [('subject', 'Subject'),
         ('course', 'Course')],
        string='Type')

    student_id = fields.Many2one(
        comodel_name='res.partner',
        string='Student')

    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course')
    record_id = fields.Many2one(
        comodel_name='education.record',
        string='Record')

    subject_id = fields.Many2one(
        comodel_name='education.subject',
        string='Subject')
    record_subject_id = fields.Many2one(
        comodel_name='education.record.subject',
        string='Record Subject')

    @api.onchange('course_id')
    def _change_course_id(self):
        if not self.course_id:
            return {'domain': {'subject_id': expression.FALSE_DOMAIN}}
        subject_fields_domain = [
            ('id', 'in', self.course_id.subject_ids.ids)]
        return {'domain': {'subject_id': subject_fields_domain}}

    @api.onchange('record_id')
    def _onchange_record_id(self):
        self.student_id = self.record_id.student_id
        self.course_id = self.record_id.course_id

    @api.onchange('record_subject_id')
    def _onchange_record_subject_id(self):
        self.student_id = self.record_subject_id.student_id
        self.course_id = self.record_subject_id.course_id
        self.subject_id = self.record_subject_id.subject_id
