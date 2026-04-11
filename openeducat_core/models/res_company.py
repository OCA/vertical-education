from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'
    signature = fields.Binary()
    accreditation = fields.Text()
    approval_authority = fields.Text()

class ResUsers(models.Model):
    _inherit = 'res.users'
    _parent_name = False

    def _department_count(self):
        return self.env['op.department'].sudo().search_count([])
    student_line = fields.Many2one('op.student', 'Line')
    user_line = fields.One2many('op.student', 'user_id', 'User Line')
    child_ids = fields.Many2many('res.users', 'res_user_first_rel1', 'user_id', 'res_user_second_rel1', string='Childs')
    dept_id = fields.Many2one('op.department', string='Department Name')
    department_ids = fields.Many2many('op.department', string='Allowed Department')
    department_count = fields.Integer(compute='_compute_department_count', string='Number of Departments', default=_department_count)

    def create_user(self, records, user_group=None):
        for rec in records:
            if not rec.user_id:
                user_vals = {'name': rec.name, 'login': rec.email or rec.name + rec.last_name, 'partner_id': rec.partner_id.id, 'dept_id': rec.main_department_id.id, 'department_ids': rec.allowed_department_ids.ids}
                user_id = self.create(user_vals)
                rec.user_id = user_id
                if user_group:
                    user_group.users = user_group.users + user_id

    def _compute_department_count(self):
        department_count = self._department_count()
        for user in self:
            user.department_count = department_count