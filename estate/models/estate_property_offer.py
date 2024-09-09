from odoo import models,fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "A property offer is an amount a potential buyer offers to the seller."

    price = fields.Float(
        string='Price',  
        default=0.00,
    )
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        string="Status", 
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    property_id = fields.Many2one("test.model", string="Property", required=True)
    
    
    
   