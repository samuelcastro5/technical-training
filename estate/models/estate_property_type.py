from odoo import models,fields,api
from odoo.osv import expression

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the property type: house, apartment, penthouse, castle"
    _order = "sequence asc"
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
    sequence = fields.Integer(string='Sequence', default=10)

    offers_count = fields.Integer(compute='_compute_offers', string="Offers")

    @api.depends('property_ids.offer_ids')
    def _compute_sale_data(self):
        for rec in self:
            cont = 0
            for l in rec.property_ids:
                cont += len(l.offer_ids)
            
            rec.offers_count = cont


    def action_view_offers(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("estate.property_offer_action")
        action['context'] = {
        }
        action['domain'] = expression.AND([[('property_id', 'in', self.property_ids.ids)]])
    
        return action