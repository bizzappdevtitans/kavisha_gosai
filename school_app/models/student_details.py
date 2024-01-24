from odoo import models, fields, api
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
    student_id = fields.Integer(string="Student ID")
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
    teacher = fields.Char(string="TeacherName", compute="compute_teacher_search")
    result = fields.One2many("result.details", "student_name", "Result")
    total_marks = fields.Float(string="Total Marks", compute="compute_total_marks")
    percentage = fields.Float(string="Percentage(%)", compute="compute_percentage")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("student_id", "UNIQUE (student_id)", "ID should be UNIQUE"),
    ]

    def compute_age(self):
        for record in self:
            today = date.today()
            if record.DOB:
                record.age = today.year - record.DOB.year
            else:
                record.age = 1

    @api.onchange("teacher_name")
    def onchange_student(self):
        self.teacher_id = self.teacher_name.ID

    def compute_subject_count(self):
        for record in self:
            subject_count = self.env["subject.details"].search_count(
                [("students", "=", record.id)]
            )
            record.subject_count = subject_count

    def compute_teacher_search(self):
        for record in self:
            teacher = self.env["teacher.details"].search(
                [("student_id", "=", record.id)]
            )
            record.teacher = teacher

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
                "domain": [("students", "=", self.id)],
                "view_type": "form",
                "view_mode": "form,tree",
                "target": "current",
            }

    def action_open_teacher_details(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Class Teacher",
            "res_model": "teacher.details",
            "res_id":"ID",
            "domain": [("student_id", "=", self.id)],
            "view_mode": "form",
            "view_type":"form",
            "target": "current",
        }

    def compute_total_marks(self):
        for record in self:
            record.total_marks = sum(line.marks for line in record.result)

    def compute_percentage(self):
        for record in self:
            record.percentage = self.total_marks / len(self.result)
