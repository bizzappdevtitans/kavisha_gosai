from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Exam Details"
    _rec_name = "subject_name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    type_of_exam = fields.Selection(
        [
            ("1st_mid", "1st MID"),
            ("2nd_mid", "2nd MID"),
            ("final", "Final"),
            ("board", "Board"),
        ],
        "Exam Type",
    )
    date = fields.Date("Date of Exam")
    subject_name = fields.Many2one(comodel_name="subject.details", string="Subject")
    teacher_id = fields.Many2one(comodel_name="teacher.details", string="Teacher")
    standard = fields.Selection(
        [
            ("1_to_5", "1 to 5"),
            ("6_to_8", "6 to 8"),
            ("9_11", "9-11"),
            ("10_12", "10-12"),
        ],
        "Standard",
    )
    active = fields.Boolean(default=True)
    exam_ref = fields.Char(
        string="Exam ID", required=True, readonly=True, default=lambda self: _("New")
    )
    teacher_phone = fields.Char(
        "TeacherPhonenumber", compute="compute_teacher_phonenumber"
    )

    @api.model
    def create(self, values):
        if values.get("exam_ref", _("New")) == _("New"):
            values["exam_ref"] = self.env["ir.sequence"].next_by_code(
                "exam.details"
            ) or _("New")
        result = super(ExamDetails, self).create(values)
        return result

    @api.onchange("standard")
    def change_exam(self):
        for record in self:
            if record.standard == "10_12":
                record.write({"type_of_exam": "board"})

    def compute_teacher_phonenumber(self):
        for record in self:
            teachers_phone = self.env["teacher.details"].search(
                [("exam_id", "=", record.id)]
            )
            record.teacher_phone = teachers_phone.mapped("phonenumber")

    def unlink(self):
        if self.type_of_exam == "board":
            raise ValidationError(("YOu can not delete this record"))
        return super(ExamDetails, self).unlink()
