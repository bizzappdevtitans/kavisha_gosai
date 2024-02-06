from odoo import models, fields, api, _


class PrincipalDetails(models.Model):
    _name = "principal.details"
    _description = "Principal Information"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    year = fields.Char("In which Year")
    principal_ref = fields.Char(
        string="Principal ID",
        required=True,
        readonly=True,
        default=lambda self: _("New"),
    )
    working_hour = fields.Char("Working Hours", compute="_compute_working_hour")

    @api.model
    def create(self, values):
        """Create a sequence number using ORM create method"""
        if values.get("principal_ref", _("New")) == _("New"):
            values["principal_ref"] = self.env["ir.sequence"].next_by_code(
                "principal.details"
            ) or _("New")
        result = super(PrincipalDetails, self).create(values)
        return result

    def _compute_working_hour(self):
        """Using System parameter write a working hours of week"""
        working_hours = self.env["ir.config_parameter"].get_param(
            "school_app.working_hour"
        )
        self.working_hour = working_hours
