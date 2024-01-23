from odoo import models, fields


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Exam Details"
    _rec_name = "subject_name"

    type_of_exam = fields.Selection(
        [("1st_mid", "1st MID"), ("2nd_mid", "2nd MID"), ("final", "Final")],
        "Exam Type",
    )
    date = fields.Date("Date of Exam")
    subject_name = fields.Many2one(comodel_name="subject.details", string="Subject")
    teacher_id = fields.Many2one(comodel_name="teacher.details", string="Teacher")
    standard = fields.Selection(
        [("1_to_5", "1 to 5"), ("6_to_10", "6 to 10"), ("11_12", "11-12")],
        "Standard",
    )
    active = fields.Boolean(default=True)
