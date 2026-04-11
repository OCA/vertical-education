# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
##############################################################################

from datetime import timedelta

from odoo import fields, models


class OpAcademicYear(models.Model):
    _name = "op.academic.year"
    _description = "Academic Year"

    name = fields.Char("Name", required=True)
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)

    term_structure = fields.Selection(
        [
            ("two_sem", "Two Semesters"),
            ("two_sem_qua", "Two Semesters subdivided by Quarters"),
            (
                "two_sem_final",
                "Two Semesters subdivided by Quarters and Final Exams",
            ),
            ("three_sem", "Three Trimesters"),
            ("four_Quarter", "Four Quarters"),
            ("final_year", "Final Year Grades subdivided by Quarters"),
            ("others", "Other(overlapping terms, custom schedules)"),
        ],
        string="Term Structure",
        default="two_sem",
        required=True,
    )
    academic_term_ids = fields.One2many(
        "op.academic.term", "academic_year_id", string="Academic Terms"
    )
    create_boolean = fields.Boolean()
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.user.company_id
    )

    def term_create(self):
        self.create_boolean = True
        if self.academic_term_ids:
            return

        structure_methods = {
            "two_sem": self._create_two_sem,
            "two_sem_qua": self._create_two_sem_qua,
            "two_sem_final": self._create_two_sem_final,
            "three_sem": self._create_three_sem,
            "four_Quarter": self._create_four_quarter,
            "final_year": self._create_final_year,
        }

        method = structure_methods.get(self.term_structure)
        if method:
            method()

    def _create_terms(self, terms_data, parent_term=None):
        academic_terms = self.env["op.academic.term"]
        for term in terms_data:
            academic_terms.create(
                {
                    "name": term["name"],
                    "term_start_date": term["from_date"],
                    "term_end_date": term["to_date"],
                    "academic_year_id": self.id,
                    "parent_term": parent_term.id if parent_term else False,
                }
            )

    def _create_two_sem(self):
        from_d = self.start_date
        to_d = self.end_date
        day = ((to_d - from_d).days + 1) / 2
        res = [
            {"name": "Semester 1", "from_date": from_d, "to_date": from_d + timedelta(days=day)},
            {"name": "Semester 2", "from_date": from_d + timedelta(days=day + 1), "to_date": to_d},
        ]
        self._create_terms(res)

    def _create_two_sem_qua(self):
        self._create_two_sem()
        num = 0
        for sub_term in self.academic_term_ids:
            delta = sub_term.term_end_date - sub_term.term_start_date
            day = (delta.days + 1) / 2
            res = [
                {
                    "name": f"Quarter {num + 1}",
                    "from_date": sub_term.term_start_date,
                    "to_date": sub_term.term_start_date + timedelta(days=day),
                },
                {
                    "name": f"Quarter {num + 2}",
                    "from_date": sub_term.term_start_date + timedelta(days=day + 1),
                    "to_date": sub_term.term_end_date,
                },
            ]
            self._create_terms(res, parent_term=sub_term)
            num += 2

    def _create_two_sem_final(self):
        self._create_two_sem()
        num = 0
        final = 1
        for sub_term in self.academic_term_ids:
            delta = sub_term.term_end_date - sub_term.term_start_date
            day = (delta.days + 1) / 2
            res = [
                {
                    "name": f"Quarter {num + 1}",
                    "from_date": sub_term.term_start_date,
                    "to_date": sub_term.term_start_date + timedelta(days=day),
                },
                {
                    "name": f"Quarter {num + 2}",
                    "from_date": sub_term.term_start_date + timedelta(days=day + 1),
                    "to_date": sub_term.term_start_date + timedelta(days=delta.days - 1),
                },
                {
                    "name": f"Final Exam {final}",
                    "from_date": sub_term.term_end_date,
                    "to_date": sub_term.term_end_date,
                },
            ]
            self._create_terms(res, parent_term=sub_term)
            num += 2
            final += 1

    def _create_three_sem(self):
        from_d, to_d = self.start_date, self.end_date
        day = ((to_d - from_d).days + 1) / 3
        res = [
            {"name": "Semester 1", "from_date": from_d, "to_date": from_d + timedelta(days=day)},
            {
                "name": "Semester 2",
                "from_date": from_d + timedelta(days=day + 1),
                "to_date": from_d + timedelta(days=2 * day + 1),
            },
            {"name": "Semester 3", "from_date": from_d + timedelta(days=2 * day + 2), "to_date": to_d},
        ]
        self._create_terms(res)

    def _create_four_quarter(self):
        from_d, to_d = self.start_date, self.end_date
        day = ((to_d - from_d).days + 1) / 4
        res = []
        for i in range(4):
            f_date = from_d + timedelta(days=i * (day + 1))
            res.append({
                "name": f"Semester {i + 1}",
                "from_date": f_date,
                "to_date": f_date + timedelta(days=day) if i < 3 else to_d
            })
        self._create_terms(res)

    def _create_final_year(self):
        self._create_terms([{"name": "Semester 1", "from_date": self.start_date, "to_date": self.end_date}])
        for sub_term in self.academic_term_ids:
            from_d, to_d = self.start_date, self.end_date
            day = ((to_d - from_d).days + 1) / 4
            res = []
            for i in range(4):
                f_date = from_d + timedelta(days=i * (day + 1))
                res.append({
                    "name": f"Quarter {i + 1}",
                    "from_date": f_date,
                    "to_date": f_date + timedelta(days=day) if i < 3 else to_d
                })
            self._create_terms(res, parent_term=sub_term)
