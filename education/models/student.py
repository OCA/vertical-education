# -*- coding: utf-8 -*-
# Copyright 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>)
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models, fields


class EducationStudentCourse(models.Model):
    _name = 'education.student.course'
    _description = 'Student Course Details'

    student_id = fields.Many2one(
        'education.student', 'Student', ondelete="cascade")
    course_id = fields.Many2one('education.course', 'Course', required=True)
    batch_id = fields.Many2one('education.batch', 'Batch', required=True)
    roll_number = fields.Char('Roll Number')
    subject_ids = fields.Many2many('education.subject', string='Subjects')

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(roll_number,course_id,batch_id,student_id)',
         'Roll Number & Student must be unique per Batch!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,batch_id)',
         'Roll Number must be unique per Batch!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]


class EducationStudent(models.Model):
    _name = 'education.student'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    course_detail_ids = fields.One2many('education.student.course',
                                        'student_id',
                                        'Course Details')
