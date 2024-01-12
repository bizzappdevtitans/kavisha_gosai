from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TeacherDetails(models.Model):
    _name = "teachers.details"
    _description = "Teacher Information"

    name = fields.Char(string="Teacher Name")
    age = fields.Integer(string="Age")
    student_id = fields.One2many("student.details", "teacher", "StudentName")
    enrollment_number = fields.Integer("Teacher ID")
    email = fields.Char(string="Email")
    website = fields.Char(string="Web site")
    subject_id = fields.One2many("subject.details","teacher_id","Subject")
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
