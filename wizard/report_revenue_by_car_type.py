from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class RevenueReportByCarTypeWizard(models.TransientModel):
    _name = "revenue.report.car.type"
    _description = "Revenue report by car type"

    car_type_id = fields.Many2one("parking.vehicle", string="Car type", required=True)
    car_type_id_relate = fields.Integer(related='car_type_id.id')

    def action_report(self):
        data = self.read()[0]
        
        car_by_type = self.env['parking.ticket'].search([("car_type_id_relate", "=", data['car_type_id_relate'])])
        price = 0

        for line in car_by_type:
            price += float(line['price'])
        data = {
            'form_data': data,
            'price': price
        }  

        return self.env.ref('intern_exercise.action_open_revenue_car_type').report_action(self, data=data)