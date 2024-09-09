from odoo import models
from logging import getLogger
from odoo import Command
_logger = getLogger(__name__)

class InheritedEstateProperty(models.Model):
    _inherit = "test.model"

    def action_sold(self):
        res =  super(InheritedEstateProperty,self).action_sold()

        self.env['account.move'].create(
            {
                "partner_id": self.buyer_id, 
                "move_type": 'out_invoice', 
                "journal_id": 1, 
                "line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.selling_price * 6 / 100,
                        }
                    ),
                    Command.create(
                        {
                            "name": "administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    )
                ],
            }
        )


        return res