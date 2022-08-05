from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class ParkingLot(models.Model):
    _name = "parking.lot"
    _description = "Parking lot"
    _rec_name = 'parking_lot_name'

    parking_lot_name = fields.Char('Parking lot name', required=True)
    working_time_from = fields.Float("Working time from", required=True)
    working_time_to = fields.Float("Working time to", required=True)
    parking_vehicle_relation_ids = fields.Many2many("lot.vehicle.relation", compute="_compute_parking_vehicle")
    parking_vehicle_ids = fields.Many2many('parking.vehicle', relation='lot_vehicle', column1='parking_lot_id', column2='parking_vehicle_id', string="Lot Vehicle")
    parking_vehicle_name_ralation = fields.Char(related="parking_vehicle_ids.parking_vehicle_name")
    total_car_now = fields.Integer("Total car", compute='_compute_total_car')
    from_date = fields.Datetime(required=False)
    to_date = fields.Datetime(required=False)
    pricelist_id = fields.Many2one("parking.pricelist", string="Price list")
    total_limit_lot = fields.Integer(string="Limit number of lot", compute="_compute_total_limit_lot")

    @api.depends("parking_vehicle_relation_ids")
    def _compute_total_limit_lot(self):
        for rec in self:
            if rec.parking_vehicle_relation_ids:
                for line in rec.parking_vehicle_relation_ids:
                    rec.total_limit_lot += line.quantity
            else:
                rec.total_limit_lot = 0

    def open_car_park(self):
        domain = [('parking_lot_id.id', '=', self.id)]
        return {
            'name': self.parking_lot_name + "'s ticket",
            'context': {'default_parking_lot_id': self.id},
            'type': 'ir.actions.act_window',
            'res_model': 'parking.ticket',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': domain,
        }

    def open_car_park_kanban(self, context=None):
        field_ids = self.env['parking.lot'].search([('id','=',self.id)])
        domain = [('id', 'not in', [field_ids.id]), ('parking_lot_id.id', '=', self.id)]

        return {
            'name': self.parking_lot_name + "'s ticket",
            'context': {
                'default_parking_lot_id': self.id, 
                'search_default_state': 'staying_in', 
            },
            'type': 'ir.actions.act_window',
            'res_model': 'parking.ticket',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': domain,
            
        }

    @api.depends("total_car_now")
    def _compute_total_car(self):
        for record in self:
            record.total_car_now = record.env['parking.ticket'].search_count([('parking_lot_id', '=', record.id)])

    @api.depends("parking_vehicle_relation_ids")
    def _compute_parking_vehicle(self):
        for rec in self:
            self.parking_vehicle_relation_ids = self.env['lot.vehicle.relation'].search([('lot.id', '=', rec.id)])

    

    
        

