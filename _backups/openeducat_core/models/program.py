from odoo import fields, models

class OpProgram(models.Model):
    _name = 'op.program'
    _inherit = 'mail.thread'
    _description = 'OpenEduCat Program'
    name = fields.Char(required=True, translate=True, tracking=True)
    code = fields.Char(size=16, required=True, translate=True)
    max_unit_load = fields.Float('Maximum Unit Load')
    min_unit_load = fields.Float('Minimum Unit Load')
    department_id = fields.Many2one('op.department', default=lambda self: self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)
    image_1920 = fields.Image('Image', attachment=True)
    program_level_id = fields.Many2one('op.program.level', required=True)

class OpProgramLevel(models.Model):
    _name = 'op.program.level'
    _inherit = 'mail.thread'
    _description = 'OpenEduCat Program level'
    name = fields.Char(required=True, translate=True, tracking=True)