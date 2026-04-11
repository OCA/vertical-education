# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
##############################################################################

from odoo import fields, models


class GradingAssigmentType(models.Model):
    _name = "grading.assignment.type"
    _description = "Assignment Type"

    name = fields.Char(required=True)
    code = fields.Char()
    assign_type = fields.Selection(
        [("sub", "Subjective"), ("attendance", "Attendance")],
        string="Type",
        default="sub",
    )
