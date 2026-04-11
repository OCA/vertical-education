from odoo import fields, models

class OpExamType(models.Model):
    _name = 'op.exam.type'
    _description = 'Exam Type'
    name = fields.Char(size=256, required=True)
    code = fields.Char(size=16, required=True)
    _sql_constraints = [('unique_exam_type_code', 'unique(code)', 'Code should be unique per exam type!')]