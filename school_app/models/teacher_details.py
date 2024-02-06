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
    teachers_rollnumber = fields.Integer(string="Teacher ID")
    phonenumber = fields.Char(string="Contact Number", required=True)
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
    principal = fields.Char("PRINCIPAL", compute="_compute_find_principal")
    student_ids = fields.One2many(
        comodel_name="student.details",
        inverse_name="teacher_id",
        string="Student Information",
    )
    subject_ids = fields.One2many(
        comodel_name="subject.details",
        inverse_name="teacher_id",
        string="Subject Information",
    )
    student_count = fields.Integer(
        string="Student count", compute="_compute_student_count"
    )
    subjects_count = fields.Integer(
        string="Subject Count", compute="_compute_subjects_count"
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
    exam_ids = fields.One2many("exam.details", "teacher_id", "ExamDuty")
    working_hour = fields.Char("Working Hours", compute="_compute_working_hour")

    @api.model
    def create(self, values):
        if values.get("teacher_ref", _("New")) == _("New"):
            values["teacher_ref"] = self.env["ir.sequence"].next_by_code(
                "teacher.details"
            ) or _("New")
        result = super(TeacherDetails, self).create(values)
        return result

    _sql_constraints = [
        ("teachers_rollnumber", "UNIQUE (teachers_rollnumber)", "ID shoul unique")
    ]

    def update_last_leave(self):
        """Update the last leave of teacher"""
        self.write({"last_leave": fields.Date.today()})

    """Create a buttons for change the state using ORM write method"""

    def primary(self):
        self.write({"state": "primary"})

    def secondary(self):
        self.write({"state": "secondary"})

    def higher_secondary(self):
        self.write({"state": "higher_secondary"})

    @api.depends("student_ids")
    def _compute_student_count(self):
        """Find the total counts of student for smart button"""
        for record in self:
            student_count = self.env["student.details"].search_count(
                [("teacher_id", "=", record.id)]
            )
            record.student_count = student_count

    def action_open_student_details(self):
        """return a form or tree view for the smart button of particular record"""
        if self.student_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "domain": [("teacher_id", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "res_id": self.student_ids.id,
                "domain": [("teacher_id", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }

    @api.depends("subject_ids")
    def _compute_subjects_count(self):
        """Find the total number of subjects for the smart button"""
        for record in self:
            subjects_count = self.env["subject.details"].search_count(
                [("teacher_id", "=", record.id)]
            )
            record.subjects_count = subjects_count

    def action_open_subjects_details(self):
        """return a form or tree view for the smart button of particular record"""
        if self.subjects_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Subjects",
                "res_model": "subject.details",
                "domain": [("teacher_id", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Subjects",
                "res_model": "subject.details",
                "res_id": self.subject_ids.id,
                "domain": [("teacher_id", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }

    @api.constrains("phonenumber")
    def check_phone(self):
        """Validate the phone number and raise the error"""
        for record in self:
            if not len(record.phonenumber) == 10:
                raise ValidationError("The phone number is not valid")
        return True

    def _default_color(self):
        return randint(1, 11)

    def name_get(self):
        """get the name as refrence number and name"""
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.teacher_ref, record.name)))
        return result

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        """search the name form name or phone number"""
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += [
                "|",
                ("name", operator, name),
                ("phonenumber", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def _compute_find_principal(self):
        """Write a principal name using serach and filtered method"""
        principal_ids = self.env["principal.details"].search([])
        for record in self:
            record.principal = principal_ids.filtered(
                lambda principal: principal.year == "2024"
            ).name

    def _compute_working_hour(self):
        """Using System parameter write a working hours of week"""
        working_hours = self.env["ir.config_parameter"].get_param(
            "school_app.working_hour"
        )
        self.working_hour = working_hours
