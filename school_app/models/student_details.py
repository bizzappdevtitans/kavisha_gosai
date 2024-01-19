from odoo import models, fields


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Student Details"
    _rec_name = "first_name"

    first_name = fields.Char(string="First Name", required=True)
    middle_name = fields.Char(string="Middle Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    address = fields.Text(string="Address")
    image = fields.Image(string="Profile")
    DOB = fields.Date(string="DOB")
    age = fields.Integer(string="Age" , readonly=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    current_standard = fields.Integer(string="Standard")
    last_year_marks = fields.Float(string="Percentage")
    last_standard = fields.Integer(string="Standard")
    priority = fields.Selection(
        [("1", "Normal"), ("2", "Good"), ("3", "Very Good"), ("4", "Excellent")],
        "Appreciation",
        default="1",
    )
    remark = fields.Html(string="Remark")
    emergency_conatct_name = fields.Char("Name")
    emergency_conatct_number = fields.Integer("Number")
    relation = fields.Char("Relation with child")

