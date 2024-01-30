from odoo import models, fields, _, api


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Exam Details"
    _rec_name = "subject_name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

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
    exam_ref = fields.Char(
        string="Exam ID", required=True, readonly=True, default=lambda self: _("New")
    )

    @api.model
    def create(self, values):
        if values.get("exam_ref", _("New")) == _("New"):
            values["exam_ref"] = self.env["ir.sequence"].next_by_code(
                "exam.details"
            ) or _("New")
        result = super(ExamDetails, self).create(values)
        return result
