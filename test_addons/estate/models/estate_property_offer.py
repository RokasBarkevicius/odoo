from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offers"

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

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(fields.Datetime.now(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days