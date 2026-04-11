from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpGradeConfiguration(models.Model):
    _name = 'op.grade.configuration'
    _rec_name = 'result'
    _description = 'Grade Configuration'
    min_per = fields.Integer('Minimum Percentage', required=True)
    max_per = fields.Integer('Maximum Percentage', required=True)
    result = fields.Char('Result to Display', required=True)

    @api.constrains('max_per')
    def max_per_validation(self):
        if self.max_per > 100:
            raise ValidationError(_('Maximum percentage should not be greater than 100'))
        if self.max_per < self.min_per:
            raise ValidationError(_('Minimum percentage should be not greater than Maximum percentage'))