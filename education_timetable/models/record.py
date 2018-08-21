from openerp import api, models, fields


class EducationRecordSubject(models.Model):
    _inherit = 'education.record.subject'

    faults = fields.Integer(
        string='Faults',
        related='last_record_subject_group_id.faults')


class EducationRecordSubjectGroup(models.Model):
    _inherit = 'education.record.subject.group'

    ausence_ids = fields.One2many(
        comodel_name='education.session.ausence',
        inverse_name='record_subject_group_id',
        string='Ausence')

    faults = fields.Integer(
        string='Faults',
        compute='_compute_faults')

    @api.multi
    def _compute_faults(self):
        for subject in self:
            subject.faults = len(subject.ausence_ids)
