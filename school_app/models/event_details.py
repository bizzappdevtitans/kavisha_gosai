from odoo import fields, models, _, api


class EventDetails(models.Model):
    _name = "event.details"
    _description = "Event Details"
    _rec_name = "event_name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    event_name = fields.Char(string="Event Name")
    standard = fields.Selection(
        [("1_to_5", "1 to 5"), ("6_to_10", "6 to 10"), ("11_12", "11-12")],
        "Standard",
    )
    sequence = fields.Integer("Sequence", default=0)
    event_date = fields.Date(string="Date of Event")
    type_of_event = fields.Selection(
        [("entertainment", "Entertainment"), ("educational", "Educational")],
        "Type Of Event",
    )
    timing = fields.Selection(
        [("morning", "Morning"), ("evening", "Evening"), ("night", "Night")], "Timing"
    )
    teacher = fields.Many2many(comodel_name="teacher.details")
    event_ref = fields.Char(
        string="Event ID", required=True, readonly=True, default=lambda self: _("New")
    )

    @api.model
    def create(self, values):
        if values.get("event_ref", _("New")) == _("New"):
            values["event_ref"] = self.env["ir.sequence"].next_by_code(
                "event.details"
            ) or _("New")
        result = super(EventDetails, self).create(values)
        return result

    @api.onchange("type_of_event")
    def change_timing(self):
        for record in self:
            if record.type_of_event == "educational":
                record.write({"timing": "morning"})
