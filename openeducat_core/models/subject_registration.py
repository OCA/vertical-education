from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpSubjectRegistration(models.Model):
    _name = 'op.subject.registration'
    _description = 'Subject Registration Details'
    _inherit = ['mail.thread']
    name = fields.Char(readonly=True, default='New')
    student_id = fields.Many2one('op.student', tracking=True)
    course_id = fields.Many2one('op.course', required=True, tracking=True)
    batch_id = fields.Many2one('op.batch', tracking=True)
    compulsory_subject_ids = fields.Many2many('op.subject', 'subject_compulsory_rel', 'register_id', 'subject_id', string='Compulsory Subjects', readonly=True)
    elective_subject_ids = fields.Many2many('op.subject', string='Elective Subjects')
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft', copy=False, tracking=True)
    max_unit_load = fields.Float('Maximum Unit Load', tracking=True)
    min_unit_load = fields.Float('Minimum Unit Load', tracking=True)
    is_read = fields.Boolean(string='Read?', default=False)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def action_reset_draft(self):
        self.state = 'draft'

    def action_reject(self):
        self.state = 'rejected'

    def action_approve(self):
        for record in self:
            subject_ids = []
            for sub in record.compulsory_subject_ids:
                subject_ids.append(sub.id)
            for sub in record.elective_subject_ids:
                subject_ids.append(sub.id)
            course_id = self.env['op.student.course'].search([('student_id', '=', record.student_id.id), ('course_id', '=', record.course_id.id)], limit=1)
            if course_id:
                course_id.write({'subject_ids': [[6, 0, list(set(subject_ids))]]})
                record.state = 'approved'
            else:
                raise ValidationError(_("Course not found on student's admission!"))

    def action_submitted(self):
        self.state = 'submitted'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('op.subject.registration') or '/'
        return super().create(vals_list)

    def get_subjects(self):
        for record in self:
            subject_ids = []
            if record.course_id and record.course_id.subject_ids:
                for subject in record.course_id.subject_ids:
                    if subject.subject_type == 'compulsory':
                        subject_ids.append(subject.id)
            record.compulsory_subject_ids = [(6, 0, subject_ids)]