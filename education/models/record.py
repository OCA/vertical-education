

from odoo import models, fields, api, _


class EducationRecord(models.Model):
    _name = 'education.record'
    _rec_name = 'code'

    code = fields.Char(
        string='Code', required=True, default=lambda self: _('New'))
    student_id = fields.Many2one(
        comodel_name='res.partner',
        string='Student', required=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course',
        required=True)
    enrollment_ids = fields.One2many(
        comodel_name='education.enrollment',
        inverse_name='record_id',
        string='Enrollments')
    record_subject_ids = fields.One2many(
        comodel_name='education.record.subject',
        inverse_name='record_id',
        string='Subjects Records')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.record') or 'New'
        return super(EducationRecord, self).create(vals)


class EducationRecordSubject(models.Model):
    _name = 'education.record.subject'
    _rec_name = 'subject_id'

    subject_id = fields.Many2one(
        comodel_name='education.subject',
        string='Subject')
    record_id = fields.Many2one(
        comodel_name='education.record',
        string='Record')
    student_id = fields.Many2one(
        comodel_name='res.partner',
        string='Student',
        related='record_id.student_id',
        readonly=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course',
        related='record_id.course_id',
        readonly=True)
    record_subject_group_ids = fields.One2many(
        comodel_name='education.record.subject.group',
        inverse_name='record_subject_id',
        string='Subjects by Group')
    last_record_subject_group_id = fields.Many2one(
        comodel_name='education.record.subject.group',
        inverse_name='record_subject_id',
        string='Last Group Record',
        compute='_compute_last_record_subject_group_id')

    @api.multi
    def _compute_last_record_subject_group_id(self):
        for record in self:
            record.last_record_subject_group_id = \
                record.record_subject_group_ids and \
                record.record_subject_group_ids[-1]


class EducationRecordSubjectGroup(models.Model):
    _name = 'education.record.subject.group'
    _rec_name = 'group_id'

    record_subject_id = fields.Many2one(
        comodel_name='education.record.subject',
        string='Subject Record')
    subject_id = fields.Many2one(
        comodel_name='education.subject',
        string='Subject',
        related='record_subject_id.subject_id',
        readonly=True)
    student_id = fields.Many2one(
        comodel_name='res.partner',
        string='Student',
        related='record_subject_id.student_id',
        readonly=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course',
        related='record_subject_id.course_id',
        readonly=True)
    enrollment_id = fields.Many2one(
        comodel_name='education.enrollment',
        string='Enrollment')
    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group',
        related='enrollment_id.group_id',
        readonly=True)
