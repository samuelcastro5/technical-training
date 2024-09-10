from datetime import datetime, date, timedelta
from odoo import models,fields,api
from odoo.exceptions import ValidationError
from logging import getLogger

_logger = getLogger(__name__)

class TestModel(models.Model):
    _name = "test.model"
    _description = "Test Model"
    _order = "id desc"

    _sql_constraints = [
        ('expected_price_check_zero',
         'CHECK(expected_price >= 0)',
         "A property expected price must be strictly positive"),
        ('selling_price_check_zero',
         'CHECK(selling_price >= 0)',
         "A property selling price must be positive"),
    ]

    name = fields.Char(
        string='Title',  
        required=True,
    )
    description = fields.Text(
        string="Description",

    )
    postcode = fields.Integer(
       string="Postcode",
    )
    available_date = fields.Date(
       string="Available From",
       copy=False,
    )
    expected_price = fields.Float(
       string= "Expected Price",
       default=0.00,
       required=True,
    )
    selling_price = fields.Float(
       string= "Selling Price",
       default=0.00,
       readonly=True,
    )
    beedrooms = fields.Integer(
       string="Beedrooms",
        default=2,
    )
    living_area = fields.Integer(
       string="Living Area (sqm)",
       default=0,
    )
    facades = fields.Integer(
       string="Facades",
       default=0,
    )
    garage = fields.Boolean(
       string="Garage",
       default=False,
    )
    garden = fields.Boolean(
       string="Garden",
       default=False,
    )
    garden_area = fields.Integer(
       string="Garden Area (sqm)",
       default=0,
    )
    active = fields.Boolean(
       string="Active",
       default=False,
    )
    status = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        string="Status", 
        default='new',
        copy=False,
        required=True,
    )
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation", 
    )

    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string='Property Type',
        ondelete='set null',
    )
    salesman_id = fields.Many2one("res.users", string="Salesman",  default=lambda self: self.env.uid)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_tag_ids = fields.Many2many('estate.property.tag', string="tags")

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string='Offers',
    )
    best_offer = fields.Float(
        string='Best Offer', 
        compute='_get_best_offer',  
        default=0.00,
    )
    total_area = fields.Integer(
       string="Total Area (sqm)",
       default=0,
       compute='_get_total_area',  
    )

    @api.depends('living_area','garden_area')
    def _get_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area


    @api.depends('offer_ids')
    def _get_best_offer(self):
        for rec in self:
            if rec.offer_ids:
                for r in rec.offer_ids.sorted(key=lambda r: (r.price), reverse=True):
                    rec.best_offer = r.price
                    break
            else:
                rec.best_offer = 0.00
    

    @api.onchange('garden')
    def onchange_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_orientation = 'north'
                rec.garden_area = 10
            else:
                rec.garden_orientation = None
                rec.garden_area = 0
    
    @api.onchange('offer_ids')
    def onchange_offer_ids(self):
        for rec in self:
            if len(rec.offer_ids) > 0:
                    rec.status="offer_received"
            else:
                rec.status="new"
    """
    @api.model_create_multi
    def create(self, values):
        if 'offer_ids' in values:
            before_offer = None
            offers = values["offer_ids"]
            for offer in offers:
                data = offer[2]
                if before_offer:
                    if before_offer != float(data["price"]):
                        raise ValidationError("It is not possible to create an offer with a lower price than an existing offer.")  
                    if before_offer < float(data["price"]):
                        before_offer = float(data["price"])
                    before_offer = float(data["price"])
        res = super(TestModel, self).create(values)
        return res
    """

    def write(self, values):
        if 'offer_ids' in values:
            offers = values["offer_ids"]
            for offer in offers:
                data = offer[2]
                for v in self.offer_ids:
                    if v.price > float(data["price"]):
                        raise ValidationError("It is not possible to create an offer with a lower price than an existing offer.")    
        res = super(TestModel, self).write(values)
        return res
    
    
    def action_cancel(self):
        self.ensure_one()
        self.status='cancelled'
    
    
    def action_sold(self):
        self.ensure_one()
        self.status='sold'

    
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            percentage = record.selling_price * 90 / 100
            if percentage > record.expected_price:
                raise ValidationError("The selling price cannot be lower than 90 percentage of the expected price.")