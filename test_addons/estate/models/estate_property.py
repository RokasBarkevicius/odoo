from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate properties"
    _order = "id desc"

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
        help="State is used to define the state of property",
        required=True,
        default="new",
        copy=False,
        readonly=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer = fields.Many2one("res.partner", string = "Buyer",copy=False)
    seller = fields.Many2one("res.users", string = "Salesman",default =lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be positive.'),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if(record.offer_ids):
                record.best_price = max(record.offer_ids.mapped("price"))
            else: record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if (self.garden == True ):
            self.garden_area = 10
            self.garden_orientation = "north"
        else:          
            self.garden_area = 0
            self.garden_orientation = ""

    def action_set_state_sold(self):
        for record in self:
            if(record.state == "canceled"):
                raise UserError("Canceled properties cannot be sold.")
            else:
                record.state = "sold"
        return True
    
    def action_set_state_canceled(self):
        for record in self:
            if(record.state == "sold"):
                raise UserError("sold properties cannot be canceled.")
            else:
                record.state = "canceled"
        return True
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) <0:
                    raise ValidationError("The selling price must be at least 90% of the expected price")
    
    @api.ondelete(at_uninstall=False)
    def remove(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError("Only new and canceled properties can be deleted")
    


