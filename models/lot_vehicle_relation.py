from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import json
    
class LotVehicleRelaion(models.Model):
    _name = "lot.vehicle.relation"
    _description = "Lot vehicle relation"
    _rec_name = 'vehicle'
    
    lot = fields.Many2one('parking.lot', 'Parking lot', ondelete='cascade')
    vehicle = fields.Many2one('parking.vehicle', 'Parking vehicle', ondelete='cascade')
    quantity = fields.Integer('Quantity')

    @api.model
    def create(self, vals):
        is_exist = self.env['lot.vehicle.relation'].search([('lot', '=', vals['lot']), ('vehicle', '=', vals['vehicle'])])
        if is_exist:
            raise ValidationError("This relation already exist")
        return super().create(vals)

