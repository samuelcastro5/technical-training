from odoo import models,fields,api
from datetime import datetime, date, timedelta
from logging import getLogger
_logger = getLogger(__name__)
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "A property offer is an amount a potential buyer offers to the seller."
    _order = "price desc"
    _sql_constraints = [
        ('offer_price_check_zero',
         'CHECK(price >= 0)',
         "An offer price must be strictly positive"),
         ('validity_check_zero',
         'CHECK(validity >= 0)',
         "A validity must be strictly positive")
    ]

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
        inverse="_inverse_date_deadline"
    )

    @api.depends('validity')
    def _get_date_deadline(self):
        for rec in self:
            rec.date_deadline = date.today() + timedelta(days=rec.validity) if not rec.id else rec.create_date + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for record in self:
            finish_date = record.create_date if record.id else date.today()
            _logger.error(record.date_deadline - finish_date.date())
            record.validity = (record.date_deadline - finish_date.date()).days


    def action_confirm(self):
        self.ensure_one()
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.selling_price = self.price
        self.property_id.status = "offer_accepted"
        

    
    def action_cancel(self):
        self.ensure_one()
        self.status="refused"