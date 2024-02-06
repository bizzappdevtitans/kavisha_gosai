from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]

    confirm_admission = fields.Integer(
        string="Admission Confirm",
        config_parameter="school_app.confirm_admission",
    )
    working_hour = fields.Selection(
        [
            ("45_hours_week", "Standard 45 Hours/Week"),
            ("40_hours_week", "Standard 40 Hours/Week"),
            ("38_hours_week", "Standard 38 Hours/Week"),
        ],
        "Working Hour",
        config_parameter="school_app.working_hour",
    )
