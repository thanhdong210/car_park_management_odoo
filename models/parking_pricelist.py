from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class ParkingPriceList(models.Model):
    _name = "parking.pricelist"
    _description = "Parking pricelist"
    _rec_name = "name"

    name = fields.Char("Pricelist name", required=True)
    parking_pricelist_item_ids = fields.One2many('parking.pricelist.item', 'parking_pricelist_id')

    
    



