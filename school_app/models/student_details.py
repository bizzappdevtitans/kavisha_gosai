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
    date_of_birth = fields.Date(string="DOB")
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    lives_hostel = fields.Boolean("Lives in School Hostel")
    current_standard = fields.Integer(string="Standard")
    last_year_marks = fields.Float(string="Percentage")
    last_standard = fields.Integer(string="standard")
    priority = fields.Selection(
        [("1", "Normal"), ("2", "Good"), ("3", "Very Good"), ("4", "Excellent")],
        "Appreciation",
        default="1",
    )
    student_rollnumber = fields.Integer("Roll Number")
    remark = fields.Html(string="Remark")
    principal = fields.Char("PRINCIPAL", compute="_compute_find_principal")
    emergency_conatct_name = fields.Char("Name")
    emergency_conatct_number = fields.Char("Number")
    relation = fields.Char("Relation with child")
    teacher_id = fields.Many2one(
        comodel_name="teacher.details",
        string="Teacher Name",
    )
    teacher_rollnumber = fields.Integer(string="Teacher ID")
    subject_ids = fields.Many2many(
        comodel_name="subject.details", domain="[('standard', '=', current_standard)]"
    )
    subject_count = fields.Integer(
        string="Subject Count", compute="_compute_subject_count"
    )
    result_ids = fields.One2many("result.details", "student_id", "Result")
    total_marks = fields.Float(string="Total Marks", compute="_compute_total_marks")
    percentage = fields.Float(string="Percentage(%)", readonly=True, default=0)
    active = fields.Boolean(default=True)
    teacher_count = fields.Integer(
        string="Teacher Count", compute="_compute_teacher_count"
    )
    student_ref = fields.Char(
        string="GR Number", required=True, readonly=True, default=lambda self: _("New")
    )

    @api.model
    def create(self, values):
        """Create a sequence number using ORM create method"""
        if values.get("student_ref", _("New")) == _("New"):
            values["student_ref"] = self.env["ir.sequence"].next_by_code(
                "student.details"
            ) or _("New")
        result = super(StudentDetails, self).create(values)
        return result

    _sql_constraints = [
        ("student_rollnumber", "UNIQUE (student_rollnumber)", "ID should unique")
    ]

    @api.depends("date_of_birth")
    def _compute_age(self):
        """Compute the age of student from the date of birth"""
        for record in self:
            today = date.today()
            if record.date_of_birth:
                record.age = today.year - record.date_of_birth.year
            else:
                record.age = 1

    @api.onchange("teacher_id")
    def onchange_teacher(self):
        """Print the teacher id from the teacher name"""
        self.teacher_rollnumber = self.teacher_id.teachers_rollnumber

    @api.depends("subject_ids")
    def _compute_subject_count(self):
        """Compute a total count of subjects for the smart button"""
        for record in self:
            subject_count = self.env["subject.details"].search_count(
                [("student_ids", "=", record.id)]
            )
            record.subject_count = subject_count

    @api.depends("teacher_id")
    def _compute_teacher_count(self):
        """Compute a total count of teacher for the smart button"""
        for record in self:
            teacher_count = self.env["teacher.details"].search_count(
                [("student_ids", "=", record.id)]
            )
            record.teacher_count = teacher_count

    def action_open_subject_details(self):
        """return a form or tree view for the smart button of particular record"""
        if self.subject_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Subjects",
                "res_model": "subject.details",
                "domain": [("student_ids", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Subjects",
                "res_model": "subject.details",
                "res_id": self.subject_ids.id,
                "domain": [("student_ids", "=", self.id)],
                "view_type": "form",
                "view_mode": "form",
                "target": "current",
            }

    def action_open_teacher_details(self):
        """return a form or tree view for the smart button of particular record"""
        if self.teacher_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Class Teacher",
                "res_model": "teacher.details",
                "domain": [("student_ids", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Class Teacher",
                "res_model": "teacher.details",
                "res_id": self.teacher_id.id,
                "domain": [("student_ids", "=", self.id)],
                "view_type": "form",
                "view_mode": "form",
                "target": "current",
            }

    @api.depends("result_ids")
    def _compute_total_marks(self):
        """find total marks from the marks of subjects"""
        for record in self:
            record.total_marks = sum(line.marks for line in record.result_ids)

    @api.depends("total_marks", "result_ids")
    def compute_percentage(self):
        """find the percentage from the total marks"""
        for record in self:
            record.percentage = self.total_marks / len(self.result_ids)

    @api.onchange("priority")
    def onchange_remark(self):
        """change the remark as nothing using ORM write method"""
        for record in self:
            if record.priority == "4":
                record.write({"remark": "Nothing"})

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, "%s - %s" % (record.student_ref, record.first_name))
            )
        return result

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += [
                "|",
                ("first_name", operator, name),
                ("current_standard", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def _compute_find_principal(self):
        """Write a principal name using serach and filtered method"""
        principal_ids = self.env["principal.details"].search([])
        for record in self:
            record.principal = principal_ids.filtered(
                lambda principal: principal.year == "2024"
            ).name
