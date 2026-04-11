from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class OpStudentCourse(models.Model):
    _name = 'op.student.course'
    _description = 'Student Course Details'
    _inherit = 'mail.thread'
    _rec_name = 'student_id'
    student_id = fields.Many2one('op.student', ondelete='cascade', tracking=True)
    course_id = fields.Many2one('op.course', required=True, tracking=True)
    batch_id = fields.Many2one('op.batch', tracking=True)
    roll_number = fields.Char(tracking=True)
    subject_ids = fields.Many2many('op.subject')
    academic_years_id = fields.Many2one('op.academic.year', 'Academic Year')
    academic_term_id = fields.Many2one('op.academic.term', 'Terms')
    state = fields.Selection([('running', 'Running'), ('finished', 'Finished')], string='Status', default='running')
    _sql_constraints = [('unique_name_roll_number_id', 'unique(roll_number,course_id,batch_id,student_id)', 'Roll Number & Student must be unique per Batch!'), ('unique_name_roll_number_course_id', 'unique(roll_number,course_id,batch_id)', 'Roll Number must be unique per Batch!'), ('unique_name_roll_number_student_id', 'unique(student_id,course_id,batch_id)', 'Student must be unique per Batch!')]

    @api.model
    def get_import_templates(self):
        return [{'label': _('Import Template for Student Course Details'), 'template': '/openeducat_core/static/xls/op_student_course.xls'}]

class OpStudent(models.Model):
    _name = 'op.student'
    _description = 'Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}
    first_name = fields.Char(translate=True)
    middle_name = fields.Char(translate=True)
    last_name = fields.Char(translate=True)
    birth_date = fields.Date()
    blood_group = fields.Selection([('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'), ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')])
    gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], required=True, default='m')
    nationality = fields.Many2one('res.country')
    emergency_contact = fields.Many2one('res.partner')
    visa_info = fields.Char(size=64)
    id_number = fields.Char('ID Card Number', size=64)
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', ondelete='cascade')
    gr_no = fields.Char('Registration Number', size=20)
    category_id = fields.Many2one('op.category')
    course_detail_ids = fields.One2many('op.student.course', 'student_id', 'Course Details', tracking=True)
    active = fields.Boolean(default=True)
    certificate_number = fields.Char(string='Certificate No.', readonly=True, copy=False)
    _sql_constraints = [('unique_gr_no', 'unique(gr_no)', 'Registration Number must be unique per student!')]

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name_1(self):
        fname = self.first_name or ''
        mname = self.middle_name or ''
        lname = self.last_name or ''
        if fname or mname or lname:
            self.name = ' '.join(filter(None, [fname, mname, lname]))
        else:
            self.name = 'New'

    def _onchange_name(self):
        return self._onchange_name_1()

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_("Birth Date can't be greater than current date!"))

    @api.model
    def get_import_templates(self):
        return [{'label': _('Import Template for Students'), 'template': '/openeducat_core/static/xls/op_student.xls'}]

    def create_student_user(self):
        user_group = self.env.ref('base.group_portal') or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({'name': record.name, 'partner_id': record.partner_id.id, 'login': record.email, 'groups_id': user_group, 'is_student': True, 'tz': self._context.get('tz')})
                record.user_id = user_id