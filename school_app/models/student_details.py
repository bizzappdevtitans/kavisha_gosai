from odoo import models, fields, api, _
from datetime import date


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Student Details"
    _rec_name = "first_name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    first_name = fields.Char(string="First Name", required=True)
    middle_name = fields.Char(string="Middle Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    address = fields.Text(string="Address")
    image = fields.Image(string="Profile")
    DOB = fields.Date(string="DOB")
    age = fields.Integer(string="Age", readonly=True, compute="compute_age")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    current_standard = fields.Integer(string="Standard")
    last_year_marks = fields.Float(string="Percentage")
    last_standard = fields.Integer(string="standard")
    priority = fields.Selection(
        [("1", "Normal"), ("2", "Good"), ("3", "Very Good"), ("4", "Excellent")],
        "Appreciation",
        default="1",
    )
    students_id = fields.Integer("Roll Number")
    remark = fields.Html(string="Remark")
    emergency_conatct_name = fields.Char("Name")
    emergency_conatct_number = fields.Integer("Number")
    relation = fields.Char("Relation with child")
    teacher_name = fields.Many2one(
        comodel_name="teacher.details",
        string="Teacher Name",
        domain="[('is_class_teacher', '=', True)]",
    )
    teacher_id = fields.Integer(string="Teacher ID")
    subject_id = fields.Many2many(
        comodel_name="subject.details", domain="[('standard', '=', current_standard)]"
    )
    subject_count = fields.Integer(
        string="Subject Count", compute="compute_subject_count"
    )
    result = fields.One2many("result.details", "student_name", "Result")
    total_marks = fields.Float(string="Total Marks", compute="compute_total_marks")
    percentage = fields.Float(string="Percentage(%)", readonly=True, default=0)
    active = fields.Boolean(default=True)
    teacher_count = fields.Integer(
        string="Teacher Count", compute="compute_teacher_count"
    )
    student_ref = fields.Char(
        string="GR Number", required=True, readonly=True, default=lambda self: _("New")
    )

    @api.model
    def create(self, values):
        if values.get("student_ref", _("New")) == _("New"):
            values["student_ref"] = self.env["ir.sequence"].next_by_code(
                "student.details"
            ) or _("New")
        result = super(StudentDetails, self).create(values)
        return result

    _sql_constraints = [("students_id", "UNIQUE (students_id)", "ID should unique")]

    def compute_age(self):
        for record in self:
            today = date.today()
            if record.DOB:
                record.age = today.year - record.DOB.year
            else:
                record.age = 1

    @api.onchange("teacher_name")
    def onchange_teacher(self):
        self.teacher_id = self.teacher_name.teachers_id

    def compute_subject_count(self):
        for record in self:
            subject_count = self.env["subject.details"].search_count(
                [("students", "=", record.id)]
            )
            record.subject_count = subject_count

    def compute_teacher_count(self):
        for record in self:
            teacher_count = self.env["teacher.details"].search_count(
                [("student_id", "=", record.id)]
            )
            record.teacher_count = teacher_count

    def action_open_subject_details(self):
        if self.subject_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Subjects",
                "res_model": "subject.details",
                "domain": [("students", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Subjects",
                "res_model": "subject.details",
                "res_id": self.subject_id.id,
                "domain": [("students", "=", self.id)],
                "view_type": "form",
                "view_mode": "form",
                "target": "current",
            }

    def action_open_teacher_details(self):
        if self.teacher_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Class Teacher",
                "res_model": "teacher.details",
                "domain": [("student_id", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Class Teacher",
                "res_model": "teacher.details",
                "res_id": self.teacher_name.id,
                "domain": [("student_id", "=", self.id)],
                "view_type": "form",
                "view_mode": "form",
                "target": "current",
            }

    def compute_total_marks(self):
        for record in self:
            record.total_marks = sum(line.marks for line in record.result)

    def compute_percentage(self):
        for record in self:
            record.percentage = self.total_marks / len(self.result)
