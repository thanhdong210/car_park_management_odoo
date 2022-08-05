from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class ParkingPriceListItem(models.Model):
    _name = "parking.pricelist.item"
    _description = "Parking pricelist item"
    _rec_name = "price"

    parking_pricelist_id = fields.Many2one('parking.pricelist')
    car_type_id = fields.Many2one("parking.vehicle")
    from_hour = fields.Float("From hour")
    to_hour = fields.Float("To hour")
    price = fields.Float("Price")
    



