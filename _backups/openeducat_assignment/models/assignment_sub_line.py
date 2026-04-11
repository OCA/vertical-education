from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpAssignmentSubLine(models.Model):
    _name = 'op.assignment.sub.line'
    _inherit = 'mail.thread'
    _rec_name = 'assignment_id'
    _description = 'Assignment Submission'
    _order = 'submission_date DESC'

    def _compute_get_user_group(self):
        for user in self:
            if self.env.user.has_group('openeducat_assignment.group_op_assignment_manager') or self.env.user.has_group('openeducat_assignment.group_op_assignment_user'):
                user.user_boolean = True
            else:
                user.user_boolean = False
    assignment_id = fields.Many2one('op.assignment', required=True)
    student_id = fields.Many2one('op.student', required=True)
    description = fields.Text(tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted'), ('reject', 'Rejected'), ('change', 'Change Req.'), ('accept', 'Accepted')], default='draft', tracking=True)
    submission_date = fields.Datetime(readonly=True, default=lambda self: fields.Datetime.now(), required=True)
    marks = fields.Float(tracking=True)
    note = fields.Text()
    user_id = fields.Many2one('res.users', related='student_id.user_id')
    faculty_user_id = fields.Many2one('res.users', related='assignment_id.faculty_id.user_id')
    user_boolean = fields.Boolean(string='Check user', compute='_compute_get_user_group')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)

    def act_draft(self):
        result = self.state = 'draft'
        return result and result or False

    def act_submit(self):
        result = self.state = 'submit'
        return result and result or False

    def act_accept(self):
        result = self.state = 'accept'
        return result and result or False

    def act_change_req(self):
        result = self.state = 'change'
        return result and result or False

    def act_reject(self):
        result = self.state = 'reject'
        return result and result or False

    @api.onchange('marks')
    def _onchange_marks(self):
        if self.assignment_id.marks < self.marks:
            raise ValidationError(_('Obtain Marks should not be greater than Actual Marks!'))
        return {}

    def unlink(self):
        for record in self:
            if not record.state == 'draft' and (not self.env.user.has_group('openeducat_assignment.group_op_assignment_user')):
                raise ValidationError(_("You can't delete none draft submissions!"))
        res = super().unlink()
        return res

    @api.model_create_multi
    def create(self, vals):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not             create Assignment Submissions!'))
        return super().create(vals)

    def write(self, vals):
        if self.env.user.child_ids:
            raise Warning(_('Invalid Action!\n Parent can not edit             Assignment Submissions!'))
        return super().write(vals)