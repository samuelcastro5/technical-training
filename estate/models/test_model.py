from odoo import models,fields

class TestModel(models.Model):
    _name = "test.model"
    _description = "Test Model"

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
    salesman_id = fields.Many2one("res.partner", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer")