from openerp import api, models, fields


class EducationRecordSubject(models.Model):
    _inherit = 'education.record.subject'

    faults = fields.Integer(
        string='Faults',
        related='last_record_subject_group_id.faults')
    cons_faults = fields.Integer(
        string='Consecutive Faults',
        related='last_record_subject_group_id.cons_faults')


class EducationRecordSubjectGroup(models.Model):
    _inherit = 'education.record.subject.group'

    ausence_ids = fields.One2many(
        comodel_name='education.session.ausence',
        inverse_name='record_subject_group_id',
        string='Ausence')

    faults = fields.Integer(
        string='Faults',
        compute='_compute_faults')
    cons_faults = fields.Integer(
        string='Consecutive faults',
        compute='_compute_cons_faults')

    @api.multi
    def _compute_faults(self):
        for subject in self:
            subject.faults = len(subject.ausence_ids)

    # TODO:
    @api.multi
    def _compute_cons_faults(self):
        timatable_obj = self.env['education.timetable.line']
        session_obj = self.env['education.session']
        for record_subject_group in self:
            timetables = timatable_obj.search([
                ('group_id', '=', record_subject_group.group_id.id),
                ('subject_id', '=', record_subject_group.subject_id.id)
            ])
            sessions = session_obj.search([
                ('timetable_id', 'in', timetables.ids),
            ]).sorted(key=lambda r: r.date)
            consecutive_faults = 0
            max_consecutive_faults = 0
            for session in sessions:
                if session.ausence_ids.filtered(
                        lambda a: a.student_id ==
                        record_subject_group.enrollment_id.student_id):
                    consecutive_faults += 1
                    if max_consecutive_faults < consecutive_faults:
                        max_consecutive_faults = consecutive_faults
                else:
                    consecutive_faults = 0
            record_subject_group.cons_faults = max_consecutive_faults
