# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
#                Luis Adan Jimenez Hernandez <luis.jimenez@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class EducationSessionAusence(models.Model):
    _name = 'education.session.ausence'
    _inherit = ['mail.thread']

    session_id = fields.Many2one(
        comodel_name='education.session',
        string='Session')

    record_subject_group_id = fields.Many2one(
        comodel_name='education.record.subject.group',
        string='Subject Record')

    student_id = fields.Many2one(
        comodel_name='res.partner',
        string='Student')

    notes = fields.Char(
        string='Notes')

    supporting_document = fields.Boolean(
        string='Supporting Document')


class EducationRecordSubjectGroup(models.Model):
    _inherit = 'education.record.subject.group'

    ausence_ids = fields.One2many(
        comodel_name='education.session.ausence',
        inverse_name='record_subject_group_id',
        string='Ausence')
