from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estatte properties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.add(fields.Datetime.now(), months=3) )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = "Orientation",
        selection=[('north', 'North'), ('east', 'East'),('south', 'South'),('west', 'West')],
        help="Orientation is used to define position of garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string = "State",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),('sold', 'Sold'),('canceled', 'Canceled')],
        help="State is used to define state of property",
        required=True,
        default="new",
        copy=False,
    )
