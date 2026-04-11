from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class GradingAssigment(models.Model):
    _name = 'grading.assignment'
    _description = 'Grading Assignment'
    name = fields.Char(required=True)
    course_id = fields.Many2one('op.course', required=True)
    subject_id = fields.Many2one('op.subject')
    issued_date = fields.Datetime(required=True)
    assignment_type = fields.Many2one('grading.assignment.type', required=True)
    faculty_id = fields.Many2one('op.faculty', default=lambda self: self.env['op.faculty'].search([('user_id', '=', self.env.uid)]), required=True)
    point = fields.Float('Points')

class OpAssignment(models.Model):
    _name = 'op.assignment'
    _inherit = 'mail.thread'
    _description = 'Assignment'
    _order = 'submission_date DESC'
    _inherits = {'grading.assignment': 'grading_assignment_id'}
    batch_id = fields.Many2one('op.batch', required=True)
    marks = fields.Float(tracking=True)
    description = fields.Text(required=True)
    state = fields.Selection([('draft', 'Draft'), ('publish', 'Published'), ('finish', 'Finished'), ('cancel', 'Cancel')], required=True, default='draft', tracking=True)
    submission_date = fields.Datetime(required=True, tracking=True)
    allocation_ids = fields.Many2many('op.student', string='Allocated To')
    assignment_sub_line = fields.One2many('op.assignment.sub.line', 'assignment_id', 'Submission')
    reviewer = fields.Many2one('op.faculty')
    active = fields.Boolean(default=True)
    grading_assignment_id = fields.Many2one('grading.assignment', required=True, ondelete='cascade')
    assignment_sub_line_count = fields.Integer('Submissions', compute='_compute_assignment_count_compute')
    courses_subjects = fields.Many2many('op.subject')

    @api.constrains('issued_date', 'submission_date')
    def check_dates(self):
        for record in self:
            issued_date = fields.Date.from_string(record.issued_date)
            submission_date = fields.Date.from_string(record.submission_date)
            if issued_date > submission_date:
                raise ValidationError(_('Submission Date cannot be set before Issue Date.'))

    def _compute_assignment_count_compute(self):
        self.assignment_sub_line_count = len(self.assignment_sub_line)

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
        if self.course_id:
            subject_ids = self.env['op.course'].search([('id', '=', self.course_id.id)]).subject_ids
            return {'domain': {'subject_id': [('id', 'in', subject_ids.ids)]}}

    @api.onchange('course_id')
    def onchange_subjects(self):
        for rec in self:
            if rec.course_id:
                rec.courses_subjects = rec.course_id.subject_ids

    def act_publish(self):
        result = self.state = 'publish'
        return result and result or False

    def act_finish(self):
        result = self.state = 'finish'
        return result and result or False

    def act_cancel(self):
        self.state = 'cancel'

    def act_set_to_draft(self):
        self.state = 'draft'

    def get_assignment_submissions(self):
        return {'name': 'Assignment Submissions', 'type': 'ir.actions.act_window', 'view_mode': 'list,form', 'res_model': 'op.assignment.sub.line', 'domain': [('id', 'in', self.assignment_sub_line.ids)], 'target': 'current'}