from odoo import api, fields, models

class OpClassroom(models.Model):
    _name = 'op.classroom'
    _description = 'Classroom'
    name = fields.Char(size=16, required=True)
    code = fields.Char(size=16, required=True)
    course_id = fields.Many2one('op.course')
    batch_id = fields.Many2one('op.batch')
    capacity = fields.Integer(string='No of Seats', required=True)
    facilities = fields.One2many('op.facility.line', 'classroom_id', string='Facility Lines')
    asset_line = fields.One2many('op.asset', 'asset_id', string='Asset')
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_classroom_code', 'unique(code)', 'Code should be unique per classroom!'), ('capacity_check', 'CHECK (capacity > 0)', 'Integer field must be greater than  0')]

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False