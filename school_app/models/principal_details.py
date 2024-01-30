from odoo import models, fields, api, _


class PrincipalDetails(models.Model):
    _name = "principal.details"
    _description = "Principal Information"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    year = fields.Char("Time Duration")
    principal_ref = fields.Char(
        string="Principal ID", required=True, readonly=True, default=lambda self: _("New")
    )

    @api.model
    def create(self, values):
        if values.get("principal_ref", _("New")) == _("New"):
            values["principal_ref"] = self.env["ir.sequence"].next_by_code(
                "principal.details"
            ) or _("New")
        result = super(PrincipalDetails, self).create(values)
        return result
