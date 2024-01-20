from odoo import models, fields


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Subject Details"
    _rec_name = "name"

    name = fields.Char(string="Name")
    standard = fields.Integer(string="Subject Standard")
    subject_teacher = fields.Many2one(
        comodel_name="teacher.details", string="Subject Teacher"
    )
    students = fields.Many2many(
        comodel_name="student.details",
    )
    student_count = fields.Integer(
        string="student Count", compute="compute_student_count"
    )

    def compute_student_count(self):
        for record in self:
            student_count = self.env["student.details"].search_count(
                [("subject_id", "=", record.id)]
            )
            record.student_count = student_count

    def action_open_student_details(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "res_model": "student.details",
            "domain": [("subject_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }
