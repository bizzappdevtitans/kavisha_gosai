from odoo import models, fields, _, api
from random import randint


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Subject Details"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    standard = fields.Integer(string="Subject Standard")
    teacher_id = fields.Many2one(
        comodel_name="teacher.details", string="Subject Teacher"
    )
    student_ids = fields.Many2many(
        comodel_name="student.details", domain="[('current_standard', '=', standard)]"
    )
    student_count = fields.Integer(
        string="student Count", compute="_compute_student_count"
    )
    teacher_count = fields.Integer(
        string="Teacher Count", compute="_compute_teacher_count"
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
    exam_date = fields.Date("ExamDate", compute="_compute_exam_date")

    @api.model
    def create(self, values):
        """Create a sequence number using ORM create method"""
        if values.get("subject_ref", _("New")) == _("New"):
            values["subject_ref"] = self.env["ir.sequence"].next_by_code(
                "subject.details"
            ) or _("New")
        result = super(SubjectDetails, self).create(values)
        return result

    @api.depends("student_ids")
    def _compute_student_count(self):
        """Find the total count of student for the smart button"""
        for record in self:
            student_count = self.env["student.details"].search_count(
                [("subject_ids", "=", record.id)]
            )
            record.student_count = student_count

    @api.depends("teacher_id")
    def _compute_teacher_count(self):
        """Find the total count of teacher for the smart button"""
        for record in self:
            teacher_count = self.env["teacher.details"].search_count(
                [("subject_ids", "=", record.id)]
            )
            record.teacher_count = teacher_count

    def action_open_student_details(self):
        """return a form or tree view for the smart button of particular record"""
        if self.student_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "domain": [("subject_ids", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Students",
                "res_model": "student.details",
                "res_id": self.student_ids.id,
                "domain": [("subject_ids", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }

    def action_open_teacher_details(self):
        """return a form or tree view for the smart button of particular record"""
        if self.teacher_count > 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Class Teacher",
                "res_model": "teacher.details",
                "domain": [("subject_ids", "=", self.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Class Teacher",
                "res_model": "teacher.details",
                "res_id": self.teacher_id.id,
                "domain": [("subject_ids", "=", self.id)],
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

    @api.depends("name")
    def _compute_exam_date(self):
        for record in self:
            exam_date = self.env["exam.details"].search(
                [("subject_id", "=", record.id)]
            )
            record.exam_date = exam_date.date

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.subject_ref, record.name)))
        return result

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += [
                "|",
                ("name", operator, name),
                ("subject_teacher", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
