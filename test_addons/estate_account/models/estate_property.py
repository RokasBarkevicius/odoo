from odoo import Command
from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_state_sold(self):
        self.env["account.move"].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids':[
                Command.create({
                    'name': self.name,
                    'quantity': 1.00,
                    'price_unit' : self.selling_price * 0.06
                }),
                Command.create({
                    'name': "Administrative fees",
                    'quantity': 1.00,
                    'price_unit' : 100.00
                })
            ]
        })
        return super().action_set_state_sold()