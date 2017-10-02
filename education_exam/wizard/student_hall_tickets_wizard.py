# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api


class StudentHallTicket(models.TransientModel):

    """ Student Hall Ticket Wizard """
    _name = 'student.hall.ticket'

    exam_session_id = fields.Many2one(
        'education.exam.session', 'Exam Session', required=True)

    @api.multi
    def print_report(self):
        data = self.read(['exam_session_id'])[0]
        return self.env['report'].get_action(
            self, 'education_exam.report_ticket', data=data)
