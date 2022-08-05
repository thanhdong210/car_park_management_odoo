from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class TicketReportWizard(models.TransientModel):
    _name = "ticket.report.wizard"
    _description = "Report parking lot"

    from_date = fields.Datetime("From Date", required=True)
    to_date = fields.Datetime("To Date", default=lambda self: fields.datetime.now())

    def multi_update(self):
        data = self.read()[0]
        #domain = [("check_in", "<", data['check_in']), ("check_out", ">", data['check_out'])]
        
        car_form_to_date = self.env['parking.ticket'].search([("check_out", ">=", data['from_date']), ("check_out", "<=", data['to_date'])])
        price = 0

        for line in car_form_to_date:
            price += float(line['price'])
        data = {
            'form_data': data,
            'price': price
        }  

        return self.env.ref('intern_exercise.action_open_report_parking_ticket').report_action(self, data=data)