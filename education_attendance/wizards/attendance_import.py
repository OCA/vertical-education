# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields, api


class OpAllStudentWizard(models.TransientModel):
    _name = 'education.all.student'

    course_id = fields.Many2one(
        'education.course', 'Course',
        default=lambda self: self.env['education.attendance.sheet'].browse(
            self.env.context['active_id']).register_id.course_id.id or False,
        readonly=True)
    batch_id = fields.Many2one(
        'education.batch', 'Batch',
        default=lambda self: self.env['education.attendance.sheet'].browse(
            self.env.context['active_id']).register_id.batch_id.id or False,
        readonly=True)
    student_ids = fields.Many2many(
        'education.student', string='Add Student(s)')

    @api.multi
    def confirm_student(self):
        for record in self:
            for sheet in self.env.context.get('active_ids', []):
                sheet_browse = self.env[
                    'education.attendance.sheet'].browse(sheet)
                absent_list = [
                    x.student_id for x in sheet_browse.attendance_line]
                all_student_search = self.env['education.student'].search(
                    [('course_detail_ids.course_id', '=',
                      sheet_browse.register_id.course_id.id),
                     ('course_detail_ids.batch_id', '=',
                      sheet_browse.register_id.batch_id.id)]
                )
                all_student_search = list(
                    set(all_student_search) - set(absent_list))
                for student_data in all_student_search:
                    vals = {'student_id': student_data.id, 'present': True,
                            'attendance_id': sheet}
                    if student_data.id in record.student_ids.ids:
                        vals.update({'present': False})
                    self.env['education.attendance.line'].create(vals)
