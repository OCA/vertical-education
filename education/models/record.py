

from odoo import models, fields, api, _


class EducationRecord(models.Model):
    _name = "education.record"
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
        string='Enrollments')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.record') or 'New'
        return super(EducationRecord, self).create(vals)


class EducationRecordSubject(models.Model):
    _name = "education.record.subject"
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
        store=True)
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course',
        related='record_id.course_id',
        store=True)
    faults = fields.Integer(
        string='Faults',
        compute='_compute_faults')
    cons_faults = fields.Integer(
        string='Consecutive faults',
        compute='_compute_cons_faults')

    @api.multi
    def _compute_faults(self):
        for subject in self:
            subject.faults = len(subject.ausence_ids)

    @api.multi
    def _compute_cons_faults(self):
        fault_prev = False
        for faults in self.subject.ausence_ids:
            if faults.subject_id == fault_prev:
                self.subject.cons_faults += 1
            fault_prev = faults.subject_id
