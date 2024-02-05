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
        "Student Standard", compute="compute_student_standard"
    )
    hostel_type = fields.Selection(
        [("boys_hostel", "Boys Hostel"), ("girls_hostel", "Girls Hostel")],
        "Hostel Type",
    )
    warden_name = fields.Char("Warden Name", compute="compute_warden_name")
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
        "Parent Phone number", readonly=True, compute="compute_parent_phone"
    )
    admission_confirm = fields.Date(
        "Admission Confirm Date", compute="confirm_admission"
    )

    def compute_warden_name(self):
        if self.hostel_type == "boys_hostel":
            self.warden_name = "HarshadSinh"
        else:
            self.warden_name = "HiralBen"

    def compute_student_standard(self):
        self.student_standard = self.student_id.current_standard

    def compute_parent_phone(self):
        self.parent_phone = self.student_id.emergency_conatct_number

    def confirm_admission(self):
        confirm_day = self.env["ir.config_parameter"].get_param(
            "school_app.cancel_admission"
        )
        confirm_date = date.today() + relativedelta.relativedelta(days=int(confirm_day))
        self.admission_confirm = confirm_date
