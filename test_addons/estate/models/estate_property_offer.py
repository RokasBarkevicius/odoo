from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string = "Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Status is used to define the status of the offer",
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", string = "Offeror",required=True)
    property_id = fields.Many2one("estate.property", string = "Property",required=True)
    validity = fields.Integer(default = 7, string = "Validity (days)")
    date_deadline = fields.Date(compute = "_compute_date_deadline", inverse = "_inverse_date_deadline")

    property_type_id= fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be positive.'),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(fields.Datetime.now(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    
    def action_confirm(self):
        for record in self:
            if any(o.status == 'accepted' for o in record.property_id.offer_ids):
                raise UserError("Only one offer can be accepted per property")
            else:
                record.status = "accepted"
                record.property_id.selling_price = self.price
                record.property_id.buyer = self.partner_id
                record.property_id.state = 'offer_accepted'
        return True
    
    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    