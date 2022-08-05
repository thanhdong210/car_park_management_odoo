from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class RevenueReportByLotWizard(models.TransientModel):
    _name = "revenue.report.lot"
    _description = "Revenue report by parking lot"

    parking_lot_id = fields.Many2one("parking.lot", string="Parking lot", required=True)
    parking_lot_id_relate = fields.Integer(related='parking_lot_id.id')
    parking_lot_name_id_relate = fields.Char(related='parking_lot_id.parking_lot_name')

    def action_report(self):
        data = self.read()[0]
        
        car_by_type = self.env['parking.ticket'].search([("parking_lot_id_relate", "=", data['parking_lot_id_relate'])])
        price = 0

        for line in car_by_type:
            price += float(line['price'])
        data = {
            'form_data': data,
            'price': price
        }  

        return self.env.ref('intern_exercise.action_open_revenue_lot').report_action(self, data=data)

    def action_report_xlsx(self):
        data = self.read()[0]
        
        car_by_type = self.env['parking.ticket'].search([("parking_lot_id_relate", "=", data['parking_lot_id_relate'])])
        price = 0

        for line in car_by_type:
            price += float(line['price'])

        list = [1, 2, 3, 4]
        data = {
            'form_data': data,
            'price': price,
            'list': list
        }  

        return self.env.ref('intern_exercise.action_open_revenue_lot_xlsx').report_action(self, data=data)