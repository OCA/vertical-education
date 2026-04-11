from odoo import fields, models

class GradingAssigmentType(models.Model):
    _name = 'grading.assignment.type'
    _description = 'Assignment Type'
    name = fields.Char(required=True)
    code = fields.Char()
    assign_type = fields.Selection([('sub', 'Subjective'), ('attendance', 'Attendance')], string='Type', default='sub')