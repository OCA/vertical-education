###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import logging

from .test_exam_common import TestExamCommon


class TestExam(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_details_of_Exam(self):
        exam = self.op_exam.search([])
        for x in exam:
            logging.info(f"Exam Name: {x.name}")
            logging.info(f"Exam Session: {x.session_id.name}")
            logging.info(f"Exam course: {x.course_id.name}")
            logging.info(f"Exam Batch: {x.batch_id.name}")
            logging.info(f"Exam subject: {x.subject_id.name}")
            logging.info(f"Exam Total Marks: {x.total_marks}")
            logging.info(f"Exam Passing Marks: {x.min_marks}")
            logging.info("Exam Attendes:")
            for attendes in x.attendees_line:
                logging.info(f" {attendes.student_id.display_name}")
            x._check_marks()
            x._check_date_time()


class TestExamAttendees(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_attendees(self):
        attendees = self.op_exam_attendees.search([])
        for _ in attendees:
            attendees._sql_constraints

            for x in attendees:
                x.onchange_exam()
                x._check_marks()


class TestExamRoom(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_attendees(self):
        room = self.op_exam_room.search([])
        for data in room:
            if not data:
                raise AssertionError("Error in data, please check for Exam Grades")
            logging.info(f"Name: {data.name}")
            logging.info(f"Room Name : {data.classroom_id.name}")
            logging.info(f"Capacity : {data.capacity}")

            for res in room:
                res.check_capacity()


class TestExamType(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_Exam_Type(self):
        exam_type = self.op_exam_type.search([])

        for data in exam_type:
            logging.info(f"Exam Type: {data.name}")
            logging.info(f"Exam code: {data.code}")


class TestGrade(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_grade(self):
        grade = self.op_grade_configuration.search([])

        if not grade:
            raise AssertionError("Error in data, please check for Exam Grades")
        for data in grade:
            logging.info(f"Min percentage : {data.min_per}")
            logging.info(f"Max percentage : {data.max_per}")
            logging.info(f"Result : {data.result}")


class TestMarksheetline(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_grade(self):
        line = self.op_marksheet_line.search([])

        for data in line:
            logging.info(f"Registration : {data.marksheet_reg_id.name}")
            logging.info(f"Evaluation Type : {data.evaluation_type}")
            logging.info(f"Percentage : {data.percentage}")
            logging.info(f"Date : {data.generated_date}")
            logging.info(f"Grade : {data.grade}")
            logging.info(f"Status : {data.status}")
            data._check_marks()
            data._compute_total_marks()
            data._compute_percentage()
            data._compute_grade()
            data._compute_status()


class TestMarksheetRegister(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_marksheet_register(self):
        register = self.op_marksheet_register.search([])

        for data in register:
            logging.info(f"Marksheet Register : {data.name}")
            logging.info(f"Exam Session : {data.exam_session_id.name}")
            for res in data.marksheet_line:
                logging.info(f"Marksheets : {res.id}")

        data._check_marks()
        data._compute_total_pass()
        data._compute_total_failed()


class TestResultLine(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_result_line(self):
        result_line = self.op_result_line.search([])
        logging.info("Marksheet Line :")
        for data in result_line:
            logging.info(f"             {data.exam_id.name}")

            data._compute_grade
            data._compute_status
            data.unlink()


class TestResultTemplate(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_result_Template(self):
        result_Template = self.op_result_template.search([])
        logging.info("Name : ")
        for data in result_Template:
            logging.info(f"    {data.name}")
            logging.info(f"State : {data.state}")
        data._check_exam_session()
        data._check_min_max_per()
        data.generate_result()


class TestExamSession(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_exam_session(self):
        exam_session = self.op_exam_session.search([])
        logging.info("Name :")
        for data in exam_session:
            logging.info(f"   {data.name}")
            logging.info(f"Start Date : {data.start_date}")
            logging.info(f"End Date : {data.end_date}")

        data._check_date_time()
        data.onchange_course()


class TestHeldExam(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_held_exam(self):
        exam = self.op_held_exam.search([])
        exam.held_exam()


class TestRoomDistribution(TestExamCommon):
    def setUp(self):
        super().setUp()

    def test_room_distribution(self):
        room = self.op_room_distribution.search([])
        for record in room:
            record._compute_get_total_student()
            record._compute_get_room_capacity()
            if record.room_ids and record.student_ids:
                record.schedule_exam()

        logging.info("computed total students")
