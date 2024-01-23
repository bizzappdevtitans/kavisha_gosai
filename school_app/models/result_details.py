from odoo import fields, models


class ResultDetails(models.Model):
    _name = "result.details"
    _description = "Result Details"

    type_of_exam = fields.Selection(
        [("1st_mid", "1st MID"), ("2nd_mid", "2nd MID"), ("final", "Final")],
        "Exam Type",
    )
    student_name = fields.Many2one(
        comodel_name="student.details",
        string="Student Name",
    )
    subject_name = fields.Many2one(
        comodel_name="subject.details",
        string="Subjects",
        domain="[('students', '=', student_name)]"
    )
    marks = fields.Integer(string="Marks")
    active = fields.Boolean(default=True)
