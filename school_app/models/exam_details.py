from odoo import models, fields


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Exam Details"
    _rec_name = "subject_name"

    type_of_exam = fields.Selection(
        [("1st_mid", "1st MID"), ("2nd_mid", "2nd MID"), ("final","Final")], "Exam Type"
    )
    date = fields.Date("Date of Exam")
    subject_name = fields.Many2one(comodel_name="subject.details",string="Subject")


