from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpExamRoom(models.Model):
    _name = 'op.exam.room'
    _description = 'Exam Room'
    name = fields.Char(size=256, required=True)
    classroom_id = fields.Many2one('op.classroom', required=True)
    capacity = fields.Integer('No of Seats', related='classroom_id.capacity', readonly=True)

    @api.onchange('classroom_id')
    def onchange_classroom(self):
        if self.classroom_id:
            self.capacity = self.classroom_id.capacity

    def check_capacity(self):
        """Check if room capacity is valid and greater than zero."""
        for rec in self:
            if rec.classroom_id and rec.capacity <= 0:
                raise ValidationError(_("Room capacity must be greater than zero for room '%s'.") % rec.name)
        return True