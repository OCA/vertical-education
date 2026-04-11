from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpLibraryCardType(models.Model):
    _name = 'op.library.card.type'
    _description = 'Library Card Type'
    name = fields.Char(size=256, required=True)
    allow_media = fields.Integer('No Of Medias Allowed', default=10, required=True)
    duration = fields.Integer(help='Duration in terms of Number of Lead Days', required=True)
    penalty_amt_per_day = fields.Float('Penalty Amount Per Day', required=True)

    @api.constrains('allow_media', 'duration', 'penalty_amt_per_day')
    def check_details(self):
        if self.allow_media < 0 or self.duration < 0.0 or self.penalty_amt_per_day < 0.0:
            raise ValidationError(_('Enter proper value'))

class OpLibraryCard(models.Model):
    _name = 'op.library.card'
    _rec_name = 'number'
    _description = 'Library Card'
    partner_id = fields.Many2one('res.partner', 'Student/Faculty', required=True)
    number = fields.Char(size=256, readonly=True)
    library_card_type_id = fields.Many2one('op.library.card.type', 'Card Type', required=True)
    issue_date = fields.Date(required=True, default=fields.Date.today())
    type = fields.Selection([('student', 'Student'), ('faculty', 'Faculty')], default='student', required=True)
    student_id = fields.Many2one('op.student', domain=[('library_card_id', '=', False)])
    faculty_id = fields.Many2one('op.faculty', domain=[('library_card_id', '=', False)])
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_library_card_number', 'unique(number)', 'Library card Number should be unique per card!')]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            x = self.env['ir.sequence'].next_by_code('op.library.card') or '/'
            vals['number'] = x
        res = super().create(vals_list)
        if res.type == 'student':
            res.student_id.library_card_id = res
        else:
            res.faculty_id.library_card_id = res
        return res

    @api.onchange('type')
    def onchange_type(self):
        self.student_id = False
        self.faculty_id = False
        self.partner_id = False

    @api.onchange('student_id', 'faculty_id')
    def onchange_student_faculty(self):
        if self.student_id:
            self.partner_id = self.student_id.partner_id
        if not self.student_id and self.faculty_id:
            self.partner_id = self.faculty_id.partner_id