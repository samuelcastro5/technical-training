from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A property tag is, for example, a property which is cozy or renovated."

    name = fields.Char(
        string='Name',  
        required=True,
    )