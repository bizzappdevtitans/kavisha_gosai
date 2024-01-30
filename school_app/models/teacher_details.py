from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from random import randint


class TeacherDetails(models.Model):
    _name = "teacher.details"
    _description = "Teacher Information"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    teachers_id = fields.Integer(string="Teacher ID")
    phone = fields.Char(string="Contact Number", required=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    state = fields.Selection(
        [
            ("primary", "Primary"),
            ("secondary", "Secondary"),
            ("higher_secondary", "Higher Secondary"),
        ],
        string="Status",
        default="primary",
    )
    is_class_teacher = fields.Boolean(string="Is Class Teacher")
    last_leave = fields.Datetime("Last Leave On")
    salary = fields.Float(string="Salary")
    student_id = fields.One2many(
        "student.details", "teacher_id", "Student Information"
    )
    subjects = fields.One2many(
        "subject.details", "subject_teacher", "Subject Information"
    )
    student_count = fields.Integer(
        string="Student count", compute="compute_student_count"
    )
    subjects_count = fields.Integer(
        string="Subject Count", compute="compute_subjects_count"
    )
    active = fields.Boolean(default=True)
    color = fields.Integer(
        string="Color Index",
        default=lambda self: self._default_color(),
        help="Tag color",
    )
    sequence = fields.Integer("Sequence", default=0)
    teacher_ref = fields.Char(
        string="GR Number", required=True, readonly=True, default=lambda self: _("New")
    )

    @api.model
    def create(self, values):
        if values.get("teacher_ref", _("New")) == _("New"):
            values["teacher_ref"] = self.env["ir.sequence"].next_by_code(
                "teacher.details"
            ) or _("New")
        result = super(TeacherDetails, self).create(values)
        return result

    _sql_constraints = [
        ('teachers_id', 'UNIQUE (teachers_id)',
            'ID shoul unique')
    ]

    def update_last_leave(self):
        self.write({"last_leave": fields.Date.today()})

    def primary(self):
        self.write({"state": "primary"})

    def secondary(self):
        self.write({"state": "secondary"})

    def higher_secondary(self):
        self.write({"state": "higher_secondary"})

    def compute_student_count(self):
        for record in self:
            student_count = self.env["student.details"].search_count(
                [("teacher_name", "=", record.id)]
            )
            record.student_count = student_count

    def action_open_student_details(self):
        if self.student_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "domain": [("teacher_name", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "res_id": self.student_id.id,
                "domain": [("teacher_name", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }

    def compute_subjects_count(self):
        for record in self:
            subjects_count = self.env["subject.details"].search_count(
                [("subject_teacher", "=", record.id)]
            )
            record.subjects_count = subjects_count

    def action_open_subjects_details(self):
        if self.subjects_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Subjects",
                "res_model": "subject.details",
                "domain": [("subject_teacher", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Subjects",
                "res_model": "subject.details",
                "res_id": self.subjects.id,
                "domain": [("subject_teacher", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }

    @api.constrains("phone")
    def check_phone(self):
        for record in self:
            if not len(record.phone) == 10:
                raise ValidationError("The phone number is not valid")
        return True

    def _default_color(self):
        return randint(1, 11)
