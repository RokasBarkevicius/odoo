from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offers"

    price = fields.Float()
    status = fields.Selection(
        string = "Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Status is used to define the status of the offer",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string = "Offeror",required=True)
    property_id = fields.Many2one("estate.property", string = "Property",required=True)

    