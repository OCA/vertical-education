from odoo import fields, models

class WizardOpFaculty(models.TransientModel):
    _name = 'wizard.op.faculty'
    _description = 'Create User for selected Faculty(s)'

    def _get_faculties(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []
    faculty_ids = fields.Many2many('op.faculty', default=_get_faculties, string='Faculties')

    def create_faculty_user(self):
        user_group = self.env.ref('openeducat_core.group_op_faculty')
        active_ids = self.env.context.get('active_ids', []) or []
        records = self.env['op.faculty'].browse(active_ids)
        self.env['res.users'].create_user(records, user_group)