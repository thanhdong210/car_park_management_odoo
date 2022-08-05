from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ParkingVehicle(models.Model):
    _name = "parking.vehicle"
    _description = "Parking vehicle"   
    _rec_name = 'parking_vehicle_name'

    parking_vehicle_name = fields.Char('Parking vehicle name', required=True)
    parking_lot_ids = fields.Many2many('parking.lot', 'lot_vehicle', column1='parking_vehicle_id', column2='parking_lot_id', string="Lot Vehicle")


    