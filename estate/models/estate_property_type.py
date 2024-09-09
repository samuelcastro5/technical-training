from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the property type: house, apartment, penthouse, castle"

    name = fields.Char(
        string='Name',  
        required=True,
    )
    property_ids = fields.One2many(
        comodel_name='test.model',
        inverse_name='property_type_id',
        string='Properties',
    )