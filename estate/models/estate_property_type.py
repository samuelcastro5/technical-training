from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the property type: house, apartment, penthouse, castle"

    _sql_constraints = [
        ('estate_name_ptype',
         'UNIQUE(name)',
         "There is already a property type with this name"),
    ]

    name = fields.Char(
        string='Name',  
        required=True,
    )
    property_ids = fields.One2many(
        comodel_name='test.model',
        inverse_name='property_type_id',
        string='Properties',
    )