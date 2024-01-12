from odoo import models, fields


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Subject Information"

    subject_name = fields.Char(string="SubjectName")
    student_id = fields.Many2many(comodel_name="student.details")
    teacher_id = fields.Many2one("teachers.details","Teacher")
    date = fields.Date(string="ExamDate")
