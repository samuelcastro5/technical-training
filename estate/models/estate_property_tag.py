from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A property tag is, for example, a property which is cozy or renovated."

    _sql_constraints = [
        ('estate_name_ptag',
         'UNIQUE(name)',
         "There is already a property tag with this name"),
    ]

    name = fields.Char(
        string='Name',  
        required=True,
    )