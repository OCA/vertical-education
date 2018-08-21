from openerp import models, fields

class EducationRecordSubjectGroup(models.Model):
    _inherit = 'education.record.subject.group'

    faults = fields.Integer(
    string='Faults',
    compute='_compute_faults')

    @api.multi
    def _compute_faults(self):
    for subject in self:
        subject.faults = len(subject.ausence_ids)
