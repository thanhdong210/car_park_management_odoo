from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class RevenueReportByLotWizardExcel(models.TransientModel):
    _name = "revenue.report.lot.xlsx"
    _description = "Revenue report by parking lot"
    _inherit = "revenue.report.lot"

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

        return self.env.ref('intern_exercise.action_open_revenue_lot_xlsx').report_action(self, data=data)