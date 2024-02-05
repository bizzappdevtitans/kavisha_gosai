# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]

    confirm_admission = fields.Integer(
        string="Admission Confirm",
        config_parameter='school_app.cancel_admission',
    )
