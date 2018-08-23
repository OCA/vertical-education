from odoo import models, api


class EducationEnrollment(models.Model):
    _inherit = "education.enrollment"

    @api.multi
    def action_done(self):
        super(EducationEnrollment, self).action_done()
        course_subject_obj = self.env['education.course.subject']
        for record_subject in self.record_id.record_subject_ids:
            course_subject = course_subject_obj.search([
                ('course_id', '=', record_subject.course_id.id),
                ('subject_id', '=', record_subject.subject_id.id),
            ])
            if course_subject:
                record_subject.write({'weight': course_subject.weight})
            for subject_group in record_subject.record_subject_group_ids:
                subject_group.grading_id = self.course_id.grading_id
        self.grading_id = self.course_id.grading_id
        self.record_id.grading_id = self.grading_id
