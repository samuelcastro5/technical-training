from odoo import models,fields
from random import randint


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A property tag is, for example, a property which is cozy or renovated."
    _order = "name"
    _sql_constraints = [
        ('estate_name_ptag',
         'UNIQUE(name)',
         "There is already a property tag with this name"),
    ]

    name = fields.Char(
        string='Name',  
        required=True,
    )

    color = fields.Integer(
        string="Color",
        default='_get_default_color',
    )

    def _get_default_color(self):
        return randint(1, 11)