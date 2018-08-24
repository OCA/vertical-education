

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EducationEnrollment(models.Model):
    _name = "education.enrollment"
    _inherit = ['mail.thread']
    _rec_name = 'code'
    _order = 'enrollment_date desc'

    code = fields.Char(
        string='Code',
        required=True,
        default=lambda self: _('New'),
        readonly=True,
        states={'draft': [('readonly', False)]})
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id.id,
        string='Company',
        readonly=True,
        states={'draft': [('readonly', False)]})
    student_id = fields.Many2one(
        comodel_name='res.partner',
        string='Student',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]})
    course_id = fields.Many2one(
        comodel_name='education.course',
        string='Course',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]})
    group_id = fields.Many2one(
        comodel_name='education.group',
        string='Group',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]})
    record_id = fields.Many2one(
        comodel_name='education.record',
        string='Record')
    subject_ids = fields.Many2many(
        comodel_name='education.subject',
        relation='enrollment_subject_rel',
        string='Subjects',
        readonly=True,
        states={'draft': [('readonly', False)]})
    enrollment_date = fields.Date(
        string='Enrollment Date')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('done', 'Done'),
         ('cancel', 'Cancelled')],
        string='Status',
        default="draft")

    @api.multi
    def action_draft(self):
        self.ensure_one()
        self.state = 'draft'

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancel'

    @api.multi
    def get_record_subject_values(self):
        record_subject_values = []
        for subject in self.subject_ids:
            record_subject_values.append(
                (0, 0, {'subject_id': subject.id})
            )
        return record_subject_values

    @api.multi
    def get_record_values(self):
        self.ensure_one()

        # TODO: Check this
        # if not self.subject_ids and not self.course_id.subject_ids\
        #         and not self.pack:
        #     raise ValidationError(
        #         _("You must add subjects to complete the enrollment"))
        return {
            'student_id': self.student_id.id,
            'course_id': self.course_id.id,
            'record_subject_ids': self.get_record_subject_values()
        }

    @api.multi
    def set_done(self):
        self.ensure_one()
        self.student_id.student = True
        self.state = 'done'

    @api.multi
    def action_done(self):
        self.ensure_one()
        record_obj = self.env['education.record']
        record = record_obj.search([
            ('student_id', '=', self.student_id.id),
            ('course_id', '=', self.course_id.id)
        ], limit=1)
        if not record:
            data = self.get_record_values()
            record = record_obj.create(data)
        record.record_subject_ids.write(
            {'record_subject_group_ids': [(0, 0, {'enrollment_id': self.id})]})
        self.record_id = record.id
        self.student_id.student = True
        self.enrollment_date = fields.Date.today()
        self.set_done()

    @api.onchange('course_id')
    def onchange_course_id(self):
        if self.course_id:
            self.subject_ids = [
                (6, 0, self.course_id.subject_ids.mapped('subject_id').ids)]
        else:
            self.subject_ids = False
        self.group_id = False

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code(
                'education.enrollment') or 'New'
        return super(EducationEnrollment, self).create(vals)

    @api.constrains('student_id', 'group_id', 'state')
    def _check_student_per_group(self):
        group_ids = self.env['education.group'].search([
            ('course_id', '=', self.group_id.course_id.id),
            ('state', '=', 'active')
        ]).ids
        other_enrollments = self.env['education.enrollment'].search([
            ('student_id', '=', self.student_id.id),
            ('group_id', 'in', group_ids),
            ('state', '=', 'done')
        ])
        if self.state == 'done' and len(other_enrollments) > 1:
            raise ValidationError(
                _("The student has already been enrolled in other group"))
