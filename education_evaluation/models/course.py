# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class EducationCourseSubject(models.Model):
    _inherit = 'education.course.subject'

    weight = fields.Float(
        string='Weight')
