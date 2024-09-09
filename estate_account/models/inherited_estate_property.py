from odoo import models
from logging import getLogger

_logger = getLogger(__name__)

class InheritedEstateProperty(models.Model):
    _inherit = "test.model"

    def action_sold(self):
        _logger.error("entro")
        res =  super(InheritedEstateProperty,self).action_sold()
        _logger.error(res)
        return res