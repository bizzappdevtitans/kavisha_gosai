from odoo import fields, models, api
from datetime import date


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Student Information"

    name = fields.Char(string="Name", required=True, size=15)
    age = fields.Integer(string="Age", compute="compute_age")
    DOB = fields.Date(string="DOB", required=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    lecture_attend = fields.Boolean("Attend Lectures", default=False)
    last_leave = fields.Datetime(
        "Last Leave On", default=lambda self: fields.Datetime.now()
    )
    priority = fields.Selection(
        [("1", "Normal"), ("2", "Good"), ("3", "Very Good"), ("4", "Excellent")],
        "Appreciation",
        default="1",
    )
    attendence = fields.Float(string="Attendance")
    remark = fields.Text(string="Remark")
    behaviour = fields.Html(string="Behaviour", help="StudentBehaviour")
    marks = fields.Float(string="Marks")
    image = fields.Image("Image")
    enrollment_number = fields.Integer("Teacher ID")
    teacher = fields.Many2one(comodel_name="teachers.details", string="Teacher Name")
    subject = fields.Many2many("subject.details")
    State = fields.Selection(
        [
            ("1st_year", "1st Year"),
            ("2nd_year", "2nd Year"),
            ("final_year", "Final Year"),
            ("done", "Graduate"),
        ],
        string="Status",
        default="current_sprint",
    )

    _sql_constraints = [
        ("name", "UNIQUE (name)", "Name already exists"),
    ]

    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.DOB:
                rec.age = today.year - rec.DOB.year
            else:
                rec.age = 1

    @api.onchange("teacher")
    def onchange_student(self):
        self.enrollment_number = self.teacher.enrollment_number

    def first_year(self):
        self.write({"State": "1st_year"})

    def second_year(self):
        self.write({"State": "2nd_year"})

    def final_year(self):
        self.write({"State": "final_year"})

    def done(self):
        self.write({"State": "done"})
