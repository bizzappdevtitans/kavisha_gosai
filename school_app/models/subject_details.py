from odoo import models, fields, _, api
from random import randint


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Subject Details"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    standard = fields.Integer(string="Subject Standard")
    subject_teacher = fields.Many2one(
        comodel_name="teacher.details", string="Subject Teacher"
    )
    students = fields.Many2many(
        comodel_name="student.details", domain="[('current_standard', '=', standard)]"
    )
    student_count = fields.Integer(
        string="student Count", compute="compute_student_count"
    )
    teacher_count = fields.Integer(
        string="Teacher Count", compute="compute_teacher_count"
    )
    active = fields.Boolean(default=True)
    color = fields.Integer(
        string="Color Index",
        default=lambda self: self._default_color(),
        help="Tag color",
    )
    subject_ref = fields.Char(
        string="Subject ID", required=True, readonly=True, default=lambda self: _("New")
    )
    exam_date = fields.Date("ExamDate",compute="compute_exam_date")

    @api.model
    def create(self, values):
        if values.get("subject_ref", _("New")) == _("New"):
            values["subject_ref"] = self.env["ir.sequence"].next_by_code(
                "subject.details"
            ) or _("New")
        result = super(SubjectDetails, self).create(values)
        return result

    def compute_student_count(self):
        for record in self:
            student_count = self.env["student.details"].search_count(
                [("subject_id", "=", record.id)]
            )
            record.student_count = student_count

    def compute_teacher_count(self):
        for record in self:
            teacher_count = self.env["teacher.details"].search_count(
                [("subjects", "=", record.id)]
            )
            record.teacher_count = teacher_count

    def action_open_student_details(self):
        if self.student_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "domain": [("subject_id", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "res_id": self.students.id,
                "domain": [("subject_id", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }

    def action_open_teacher_details(self):
        if self.teacher_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Class Teacher",
                "res_model": "teacher.details",
                "domain": [("subjects", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Class Teacher",
                "res_model": "teacher.details",
                "res_id": self.subject_teacher.id,
                "domain": [("subjects", "=", self.id)],
                "view_type": "form",
                "view_mode": "form",
                "target": "current",
            }

    def _default_color(self):
        return randint(1, 11)

    @api.onchange("name")
    def change_color(self):
        for record in self:
            if record.name == "English":
                record.write({"color": 4})

    def compute_exam_date(self):
        for record in self:
            exam_date = self.env["exam.details"].search(
                [("subject_name", "=", record.id)]
            )
            record.exam_date = exam_date.date

