from odoo import fields, models


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
    event_date = fields.Date(string="Date of Event")
    type_of_event = fields.Selection(
        [("entertainment", "Entertainment"), ("educational", "Educational")],
        "Type Of Event",
    )
    timing = fields.Selection(
        [("morning", "Morning"), ("evening", "Evening"), ("night", "Night")], "Timing"
    )
    teacher = fields.Many2many(comodel_name="teacher.details")
