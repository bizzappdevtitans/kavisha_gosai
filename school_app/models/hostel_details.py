from odoo import models, fields, api
from datetime import date
from dateutil import relativedelta


class HostelDetails(models.Model):
    _name = "hostel.details"
    _description = "Hostel Details"

    student_id = fields.Many2one(
        "student.details", "Student Name", domain="[('lives_hostel','=',True)]"
    )
    student_standard = fields.Integer(
        "Student Standard", compute="_compute_student_standard"
    )
    hostel_type = fields.Selection(
        [("boys_hostel", "Boys Hostel"), ("girls_hostel", "Girls Hostel")],
        "Hostel Type",
    )
    warden_name = fields.Char("Warden Name", compute="_compute_warden_name")
    total_fees = fields.Integer("Total Fees")
    floor = fields.Selection(
        [
            ("1st_floor", "1st Floor"),
            ("2nd_floor", "2nd Floor"),
            ("3rd_floor", "3rd Floor"),
        ],
        "Floor",
    )
    room_number = fields.Integer("Room number")
    parent_phone = fields.Char(
        "Parent Phone number", readonly=True, compute="_compute_parent_phone"
    )
    admission_confirm = fields.Date(
        "Admission Confirm Date", compute="_compute_confirm_admission"
    )

    @api.depends("warden_name")
    def _compute_warden_name(self):
        """Change the warden name"""
        if self.hostel_type == "boys_hostel":
            self.warden_name = "HarshadSinh"
        else:
            self.warden_name = "HiralBen"

    @api.depends("student_id")
    def _compute_student_standard(self):
        """Write the student standard according to student name"""
        self.student_standard = self.student_id.current_standard

    @api.depends("student_id")
    def _compute_parent_phone(self):
        """Write a parent's phone number from the student name"""
        self.parent_phone = self.student_id.emergency_conatct_number

    @api.depends("admission_confirm")
    def _compute_confirm_admission(self):
        """Using System Parameter print the admission confirm date"""
        confirm_day = self.env["ir.config_parameter"].get_param(
            "school_app.confirm_admission"
        )
        confirm_date = date.today() + relativedelta.relativedelta(days=int(confirm_day))
        self.admission_confirm = confirm_date
