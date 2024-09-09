from odoo import models,fields,api
from datetime import datetime, date, timedelta

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
    
    
    validity = fields.Integer(
        string='Validity (Days)',  
        default = 7,
    )

    date_deadline = fields.Date(
        string='Deadline',  
        default= date.today(),
        compute='_get_date_deadline',  
    )

    @api.depends('validity')
    def _get_date_deadline(self):
        for rec in self:
            rec.date_deadline =date.today() + timedelta(days=rec.validity)

    def action_confirm(self):
        self.ensure_one()
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.selling_price = self.price
        

    
    def action_cancel(self):
        self.ensure_one()
        self.status="refused"