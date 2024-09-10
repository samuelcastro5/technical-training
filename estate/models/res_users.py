from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    
    def _get_domain(self):
        return [('status', 'in', ['new', 'offer_received'])]
    properties_ids = fields.One2many('test.model', 'salesman_id', string='Real Estate Properties', domain=_get_domain)
   