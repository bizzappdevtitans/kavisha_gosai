from odoo import models, fields


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Subject Information"

    subject_name = fields.Char(string="SubjectName")
    student_id = fields.Many2many(comodel_name="student.details")
    teacher_id = fields.Many2one("teachers.details", "Teacher", ondelete="cascade")
    date = fields.Date(string="ExamDate")
    student_count = fields.Integer(
        string="Student Count", compute="compute_student_count"
    )

    def compute_student_count(self):
        for record in self:
            student_count = self.env["student.details"].search_count(
                [("subject", "=", record.id)]
            )
            record.student_count = student_count

    def action_open_student_details(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "res_model": "student.details",
            "domain": [("subject", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
        }
