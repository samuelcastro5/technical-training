from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

   
    properties_ids = fields.One2many('test.model', 'salesman_id', string='Real Estate Properties')
   