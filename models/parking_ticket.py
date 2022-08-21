from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import random
import string
import pytz

class ParkingTicket(models.Model):
    _name = "parking.ticket"
    _description = "Parking ticket"
    _rec_name = 'parking_ticket_name'

    parking_ticket_name = fields.Char('Car name', required=True)
    parking_lot_id = fields.Many2one('parking.lot', required=True)
    parking_lot_id_relate = fields.Integer(related='parking_lot_id.id')
    car_image = fields.Binary("Car Image", attachment=True, help="Car Image")
    car_type_id = fields.Many2one("parking.vehicle", required=True)
    check_in = fields.Datetime("Check in", required=True)
    check_out = fields.Datetime("Checkout")
    total_time = fields.Char("Total time")
    code = fields.Char("Code", readonly=True)
    price = fields.Float("Price")
    state = fields.Selection([
                ('checked_out', "Checked out"),
                ('staying_in', "Staying in")
            ], default='staying_in')

    @api.onchange('car_type_id')
    def _domain_parking_vehicle_type(self):
        car_type_ids = self.env['parking.lot'].search([('id', '=', self.env.context.get('default_parking_lot_id'))]).parking_vehicle_relation_ids.vehicle
        domain = {'car_type_id': [('id', 'in', car_type_ids.ids)]}
        return {'domain': domain}  

    def action_check_out(self):  
        self.check_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d1 = datetime.strptime(str(self.check_in),'%Y-%m-%d %H:%M:%S') 
        d2 = datetime.strptime(str(self.check_out),'%Y-%m-%d %H:%M:%S')       
        d3 = d2 - d1
        delta = d3 / timedelta(hours=1)      
        delta2 = str(round(delta, 0))

        #price
        global price1
        price1 = 0
        for record in self:
            line = self.env['parking.pricelist.item'].search([('car_type_id', '=', record.car_type_id.id), ('parking_pricelist_id.id', '=', record.parking_lot_id.pricelist_id.id)])
            for row in line:
                if float(record.total_time) >= row.from_hour and float(record.total_time) <= row.to_hour:                    
                    price1 = row.price
                self.write(vals={'total_time': delta2, 'price': price1, 'state': 'checked_out'})

        return {
            'name': "Checkout",
            'context': {'default_price': self.price, 'default_total_time': self.total_time},
            'type': 'ir.actions.act_window',
            'res_model': 'checkout.action',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'views': [(False, 'form')],
        }

    def _check_lot_is_full(self, parking_ticket, parking_lot):
        total_car_type_in_lot = self.env['parking.ticket'].search_count([('car_type_id', '=', parking_ticket), ('parking_lot_id', '=', parking_lot), ('check_out', '!=', False)])
        total_car_type_in_lot_limit = self.env['lot.vehicle.relation'].search([('lot', '=', parking_lot), ('vehicle', '=', parking_ticket)], limit=1).quantity
        if total_car_type_in_lot_limit <= total_car_type_in_lot:
            return False

        total_limit_lot = self.env['parking.lot'].search([('id', '=', parking_lot)]).total_limit_lot
        total_car_in_lot = self.env['parking.lot'].search([('id', '=', parking_lot)]).total_car_now
        if total_car_in_lot >= total_limit_lot:
            return False
        return True

    def _check_is_still_in_working_time(self):
        working_time_to = self.env['parking.lot'].search([('id', '=', self.env.context.get('default_parking_lot_id'))]).working_time_to
        working_time_from = self.env['parking.lot'].search([('id', '=', self.env.context.get('default_parking_lot_id'))]).working_time_from
        local = self.env.user.tz
        now_utc = datetime.now(timezone('UTC'))
        now_asia = now_utc.astimezone(timezone(local))
        if now_asia.hour >= working_time_to or now_asia.hour < working_time_from:
            return True
        return False

    @api.model
    def create(self, vals):
        # Compute is number of ticket in this lot is full
        if self._check_lot_is_full(vals['car_type_id'], self.env.context.get('default_parking_lot_id')) == False:
            raise ValidationError('This lot is full')

        # Compute is checkin of parking ticket still in working time
        if self._check_is_still_in_working_time():
            raise ValidationError('Not in working time')

        # Create ref code for parking ticket
        vals['code'] = self.create_ref_code()
        return super().create(vals)

    def create_ref_code(self):
        now= datetime.strftime(fields.Datetime.context_timestamp(self, datetime.now()), "%Y-%m-%d %H:%M:%S")
        now2 = now.split("-")
        now3 = ""
        for l in now2:
            now3 += l
        now4 = now3[:10]
        random1 = ''.join(random.choices(string.digits, k = 7))
        code = now4 + str(random1)
        return code

    

