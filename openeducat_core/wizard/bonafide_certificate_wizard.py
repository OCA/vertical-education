from odoo import _, api, fields, models
from odoo.exceptions import UserError


class BonafideCertificateWizard(models.TransientModel):
    _name = 'bonafide.certificate.wizard'
    _description = 'Bonafide Certificate Wizard'

    student_ids = fields.Many2many('op.student', string='Students', required=True)

    certificate_purpose = fields.Selection([
        ('passport', 'Passport Application'),
        ('bank_account', 'Bank Account Opening'),
        ('scholarship', 'Scholarship'),
        ('internship', 'Internship'),
        ('visa', 'Visa'),
        ('address_proof', 'Address Proof'),
        ('other', 'Other')
    ], string='Certificate Purpose', required=True, default='passport')
    other_purpose = fields.Char(
        'Other Purpose', help='Specify other purpose if selected')

    @api.model
    def default_get(self, fields):
        """Get default values for the wizard."""
        res = super(BonafideCertificateWizard, self).default_get(fields)
        active_id = self.env.context.get('active_ids', False)
        if active_id:
            res['student_ids'] = [(6, 0, active_id)]
        return res

    def action_print_bonafide_certificate(self):
        """Print bonafide certificate with purpose."""
        students = self.student_ids
        if not students and self.env.context.get('active_ids'):
            students = self.env['op.student'].browse(self.env.context['active_ids'])
        if not students:
            raise UserError(_("No students selected for the certificate."))
        for student in students:
            if not student.certificate_number:
                student.certificate_number = (
                    self.env['ir.sequence']
                    .next_by_code('op.student.certificate')
                )
        action = (
            self.env.ref('openeducat_core.action_report_student_bonafide')
            .report_action(
                students.ids,
                data={
                    'certificate_purpose': self.certificate_purpose,
                    'other_purpose': self.other_purpose,
                    'purpose_display': self._get_purpose_display()
                }
            )
        )
        action['close_on_report_download'] = True
        return action

    def _get_purpose_display(self):
        """Get the display text for the selected purpose."""
        purpose_mapping = {
            'passport': 'Passport Application',
            'bank_account': 'Bank Account Opening',
            'scholarship': 'Scholarship',
            'internship': 'Internship',
            'visa': 'Visa',
            'address_proof': 'Address Proof',
            'other': self.other_purpose or 'Other'
        }
        return purpose_mapping.get(self.certificate_purpose, 'Other')
