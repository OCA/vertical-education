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
            ("two_sem_qua", "Two Semesters Subdivision"),
            ("two_sem_final", "Two Semesters Subdivision Final"),
            ("three_sem", "Three Trimesters"),
            ("four_Quarter", "Four Quarters"),
            ("final_year", "Final Year Grades Subdivision"),
            ("others", "Other (overlapping terms, custom schedules)"),
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
        """Action button to create terms based on structure"""
        self.create_boolean = True
        if self.academic_term_ids:
            return

        if self.term_structure == "two_sem":
            self._handle_two_sem()
        elif self.term_structure == "two_sem_qua":
            self._handle_two_sem_qua()
        elif self.term_structure == "two_sem_final":
            self._handle_two_sem_final()
        elif self.term_structure == "three_sem":
            self._handle_three_sem()
        elif self.term_structure == "four_Quarter":
            self._handle_four_quarter()
        elif self.term_structure == "final_year":
            self._handle_final_year()

    def _handle_two_sem(self):
        from_d, to_d = self.start_date, self.end_date
        day = ((to_d - from_d).days + 1) / 2
        res = [
            {"name": "Semester 1", "from_d": from_d, "to_d": from_d + timedelta(days=day)},
            {"name": "Semester 2", "from_d": from_d + timedelta(days=day + 1), "to_d": to_d},
        ]
        for term in res:
            self.env["op.academic.term"].create({
                "name": term["name"],
                "term_start_date": term["from_d"],
                "term_end_date": term["to_d"],
                "academic_year_id": self.id,
            })

    def _handle_two_sem_qua(self):
        from_d, to_d = self.start_date, self.end_date
        day = ((to_d - from_d).days + 1) / 2
        res = [
            {"name": "Semester 1", "from_d": from_d, "to_d": from_d + timedelta(days=day)},
            {"name": "Semester 2", "from_d": from_d + timedelta(days=day + 1), "to_d": to_d},
        ]
        num = 0
        for term in res:
            parent = self.env["op.academic.term"].create({
                "name": term["name"],
                "term_start_date": term["from_d"],
                "term_end_date": term["to_d"],
                "academic_year_id": self.id,
            })
            # Original Logic: Loop over ALL children of the year
            for sub_term in self.academic_term_ids:
                if sub_term.id != parent.id:
                    continue
                s_from, s_to = sub_term.term_start_date, sub_term.term_end_date
                s_day = ((s_to - s_from).days + 1) / 2
                quarters = [
                    {"name": f"Quarter {num + 1}", "f": s_from, "t": s_from + timedelta(days=s_day)},
                    {"name": f"Quarter {num + 2}", "f": s_from + timedelta(days=s_day + 1), "t": s_to},
                ]
                for q in quarters:
                    self.env["op.academic.term"].create({
                        "name": q["name"],
                        "term_start_date": q["f"],
                        "term_end_date": q["t"],
                        "academic_year_id": self.id,
                        "parent_term": sub_term.id,
                    })
                num += 2

    def _handle_two_sem_final(self):
        # Implementation mirroring original structure
        self._handle_two_sem()
        num, final = 0, 1
        for sub_term in self.academic_term_ids:
            s_from, s_to = sub_term.term_start_date, sub_term.term_end_date
            s_day = ((s_to - s_from).days + 1) / 2
            quarters = [
                {"name": f"Quarter {num + 1}", "f": s_from, "t": s_from + timedelta(days=s_day)},
                {"name": f"Quarter {num + 2}", "f": s_from + timedelta(days=s_day + 1), "t": s_from + timedelta(days=(s_to - s_from).days - 1)},
                {"name": f"Final Exam {final}", "f": s_to, "t": s_to},
            ]
            for q in quarters:
                self.env["op.academic.term"].create({
                    "name": q["name"],
                    "term_start_date": q["f"],
                    "term_end_date": q["t"],
                    "academic_year_id": self.id,
                    "parent_term": sub_term.id,
                })
            num += 2
            final += 1

    def _handle_three_sem(self):
        from_d, to_d = self.start_date, self.end_date
        day = ((to_d - from_d).days + 1) / 3
        res = [
            {"name": "Semester 1", "f": from_d, "t": from_d + timedelta(days=day)},
            {"name": "Semester 2", "f": from_d + timedelta(days=day + 1), "t": from_d + timedelta(days=day * 2 + 1)},
            {"name": "Semester 3", "f": from_d + timedelta(days=day * 2 + 2), "t": to_d},
        ]
        for t in res:
            self.env["op.academic.term"].create({
                "name": t["name"],
                "term_start_date": t["f"],
                "term_end_date": t["t"],
                "academic_year_id": self.id,
            })

    def _handle_four_quarter(self):
        from_d, to_d = self.start_date, self.end_date
        day = ((to_d - from_d).days + 1) / 4
        res = []
        for i in range(4):
            f = from_d + timedelta(days=i * (day + 1))
            t = f + timedelta(days=day) if i < 3 else to_d
            res.append({"name": f"Semester {i + 1}", "f": f, "t": t})
        for t in res:
            self.env["op.academic.term"].create({
                "name": t["name"],
                "term_start_date": t["f"],
                "term_end_date": t["t"],
                "academic_year_id": self.id,
            })

    def _handle_final_year(self):
        self.env["op.academic.term"].create({"name": "Semester 1", "term_start_date": self.start_date, "term_end_date": self.end_date, "academic_year_id": self.id})
        for sub_term in self.academic_term_ids:
            day = ((sub_term.term_end_date - sub_term.term_start_date).days + 1) / 4
            for i in range(4):
                f = sub_term.term_start_date + timedelta(days=i * (day + 1))
                t = f + timedelta(days=day) if i < 3 else sub_term.term_end_date
                self.env["op.academic.term"].create({"name": f"Quarter {i + 1}", "term_start_date": f, "term_end_date": t, "academic_year_id": self.id, "parent_term": sub_term.id})
