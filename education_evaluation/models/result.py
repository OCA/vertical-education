
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    grading_id = fields.Many2one(
        string='Grading',
        comodel_name='education.grading.scale',
        readonly=True)
    grade_id = fields.Many2one(
        string='Grade',
        comodel_name='education.grade',
        compute='_compute_grade')

    @api.constrains('score_manual')
    def _check_field(self):
        dec = str(self.score_manual).split(".")[1]
        if dec.__len__() > self.grading_id.decimals_number:
            raise ValidationError(
             "Max "+str(self.exam_id.grading_id.decimals_number)+" decimals")

    @api.multi
    @api.depends('score_type', 'score_manual', 'score_computed')
    def _compute_score(self):
        for evaluable in self:
            evaluable.score_computed = evaluable.score_computed
            evaluable.score = evaluable.score_type == 'computed' and \
                evaluable.score_computed or evaluable.score_manual

    @api.multi
    def _compute_score_computed(self):
        for evaluable in self:
            evaluable.score_computed = round(
                evaluable.score_computed, evaluable.grading_id.
                decimals_number)

    @api.multi
    def _compute_grade(self):
        for result in self:
            for grade in result.grading_id.grade_ids:
                if result.score >= grade.start:
                    result.grade_id = grade


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

    grade_id = fields.Many2one(
        string='Grade',
        comodel_name='education.grade',
        compute='_compute_grade')

    @api.multi
    def _compute_grade(self):
        for result in self:
            for grade in result.exam_id.grading_id.grade_ids:
                if result.score <= grade.end:
                    result.grade_id = grade

    @api.constrains('score')
    def _check_field(self):
        dec = str(self.score).split(".")[1]
        if dec.__len__() > self.exam_id.grading_id.decimals_number:
            raise ValidationError(
             "Max "+str(self.exam_id.grading_id.decimals_number)+" decimals")


class EducationRecordSubject(models.Model):
    _inherit = 'education.record.subject'

    weight = fields.Float(
        string='Weight',
        readonly=True)
    score = fields.Float(
        string='Score',
        related='last_record_subject_group_id.score',
        readonly=True)
    grade_id = fields.Many2one(
        string='Grade',
        related='last_record_subject_group_id.grade_id',
        comodel_name='education.grade',
        readonly=True)


class EducationRecordSubjectGroup(models.Model):
    _name = 'education.record.subject.group'
    _inherit = ['education.record.subject.group', 'education.evaluable']

    evaluation_result_ids = fields.One2many(
        comodel_name='education.result',
        inverse_name='record_subject_group_id',
        string='Evaluations')

    weight = fields.Float(
        string='Weight',
        related='record_subject_id.weight',
        readonly=True)

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
