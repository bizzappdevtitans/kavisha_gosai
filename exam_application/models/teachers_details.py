from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TeacherDetails(models.Model):
    _name = "teachers.details"
    _description = "Teacher Information"
    _inherit = ["mail.thread","mail.activity.mixin"]

    name = fields.Char(string="Teacher Name")
    age = fields.Integer(string="Age")
    student_id = fields.One2many("student.details", "teacher", "StudentName")
    student_count = fields.Integer(
        string="Student Count", compute="compute_student_count"
    )
    subjects_count = fields.Integer(
        string="Subject Count", compute="compute_subjects_count"
    )
    enrollment_number = fields.Integer(string="Teacher ID")
    email = fields.Char(string="Email")
    website = fields.Char(string="Web site")
    subject_id = fields.One2many("subject.details", "teacher_id", "Subject")
    phone = fields.Char(string="Mobile Number")
    state = fields.Selection(
        [
            ("current_sprint", "Current Sprint"),
            ("in_progress", "In Progress"),
            ("cancel", "Cancelled"),
            ("done", "Done"),
        ],
        string="Status",
        default="current_sprint",
    )

    @api.constrains("phone")
    def check_phone(self):
        for record in self:
            if record.phone and len(record.phone) != 10:
                raise ValidationError("The phone number is not valid")
        return True

    def compute_student_count(self):
        for record in self:
            student_count = self.env["student.details"].search_count(
                [("teacher", "=", record.id)]
            )
            record.student_count = student_count

    def compute_subjects_count(self):
        for record in self:
            subjects_count = self.env["subject.details"].search_count(
                [("teacher_id", "=", record.id)]
            )
            record.subjects_count = subjects_count

    def action_open_student_details(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "res_model": "student.details",
            "domain": [("teacher", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }

    def action_open_subjects_details(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Subjects",
            "res_model": "subject.details",
            "domain": [("teacher_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }
