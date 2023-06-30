from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property types"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")

    property_ids = fields.One2many("estate.property", "property_type_id")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_counts = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The type must be unique.'),
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_counts = len(record.offer_ids)

    def action_preview_offers(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }
