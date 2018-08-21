
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class EducationEvaluable(models.AbstractModel):
    _name = 'education.evaluable'

    score_type = fields.Selection(
        [('manual', 'Manual'),
         ('computed', 'Computed')],
        default='manual',
        string='Score type',
        required=True)
    score = fields.Float(
        string='Score',
        compute='_compute_score')
    score_computed = fields.Float(
        string='Computed Score',
        compute='_compute_score_computed')
    score_manual = fields.Float(
        string='Score')

    @api.multi
    @api.depends('score_type', 'score_manual', 'score_computed')
    def _compute_score(self):
        for evaluable in self:
            evaluable.score_computed = evaluable.score_computed
            evaluable.score = evaluable.score_type == 'computed' and \
                evaluable.score_computed or evaluable.score_manual

    @api.multi
    def _compute_score_computed(self):
        pass


class EducationResult(models.Model):
    _name = 'education.result'
    _inherit = ['mail.thread']

    exam_id = fields.Many2one(
        comodel_name='education.exam',
        string='Exam')

    score = fields.Float(
        string='Score')

    record_subject_group_id = fields.Many2one(
        comodel_name='education.record.subject.group',
        string='Subject Record')

    student_id = fields.Many2one(
        comodel_name='res.partner',
        string='Student',
        related='record_subject_group_id.record_subject_id.'
                'record_id.student_id')

    weight = fields.Float(
        string='Weight',
        related='exam_id.weight',
        readonly=True)


class EducationRecordSubject(models.Model):
    _name = 'education.record.subject'
    _inherit = ['education.record.subject', 'education.evaluable']

    evaluation_result_ids = fields.One2many(
        comodel_name='education.result',
        inverse_name='record_subject_group_id',
        string='Evaluations')

    weight = fields.Float(
        string='Weight',
        readonly=True)

    @api.multi
    def _compute_weight(self):
        for record in self:
            record.weight = record.subject_id

    @api.multi
    @api.depends('evaluation_result_ids.exam_id.weight',
                 'evaluation_result_ids.score')
    def _compute_score_computed(self):
        for record in self:
            exams = record.evaluation_result_ids
            total_weight = sum(exams.mapped('exam_id.weight'))
            record.score_computed = sum(exams.mapped(
                lambda e: e.exam_id.weight * e.score
            )) / (total_weight or 1)


class EducationRecord(models.Model):
    _name = 'education.record'
    _inherit = ['education.record', 'education.evaluable']

    @api.multi
    @api.depends('record_subject_ids.weight',
                 'record_subject_ids.score')
    def _compute_score_computed(self):
        for record in self:
            subjects = record.record_subject_ids
            total_weight = sum(subjects.mapped('weight'))
            record.score_computed = sum(subjects.mapped(
                lambda e: e.weight * e.score
            )) / (total_weight or 1)
