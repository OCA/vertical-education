from odoo import _, api, fields, models

class OpSubject(models.Model):
    _name = 'op.subject'
    _inherit = 'mail.thread'
    _description = 'Subject'
    name = fields.Char(size=128, required=True)
    code = fields.Char(size=256, required=True)
    grade_weightage = fields.Float()
    type = fields.Selection([('theory', 'Theory'), ('practical', 'Practical'), ('both', 'Both'), ('other', 'Other')], default='theory', required=True)
    subject_type = fields.Selection([('compulsory', 'Compulsory'), ('elective', 'Elective')], default='compulsory', required=True)
    department_id = fields.Many2one('op.department', default=lambda self: self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_subject_code', 'unique(code)', 'Code should be unique per subject!')]

    @api.model
    def get_import_templates(self):
        return [{'label': _('Import Template for Subjects'), 'template': '/openeducat_core/static/xls/op_subject.xls'}]