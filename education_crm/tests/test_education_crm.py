
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import TransactionCase


class TestEducationCRM(TransactionCase):

    def setUp(self):
        super(TestEducationCRM, self).setUp()
        self.lead_obj = self.env['crm.lead']
        self.course = self.env.ref('education.education_course_1')
        self.enrollment = self.env.ref('education.education_enrollment_1')

    def test_create_enrollment(self):
        lead = self.lead_obj.create({
            'name': 'Test Enrollment',
            'course_id': self.course.id,
            'enrollment_id': self.enrollment.id
        })
        lead.create_enrollment()
