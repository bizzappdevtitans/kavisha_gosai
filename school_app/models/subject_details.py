from odoo import models, fields


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
