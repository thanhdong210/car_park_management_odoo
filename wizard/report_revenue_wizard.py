from email.policy import default
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from datetime import timedelta

import logging

from odoo.tools.misc import groupby
_logger = logging.getLogger(__name__)

class RevenueReportByLotWizard(models.TransientModel):
    _name = "report.revenue"
    _description = "Revenue report"

    report_types = fields.Selection([
        ('by_day', "By 7 days"),
        ('by_month', "By 4 week in a month"),
        ('by_year', "By 12 months in a year"),
    ], default='by_date')

    check_day = fields.Boolean(default=True)
    check_month = fields.Boolean(default=True)
    check_year = fields.Boolean(default=True)

    day = fields.Datetime("Choose day", default=lambda self: fields.datetime.now())
    month_by_month = fields.Datetime("Choose month", default=lambda self: fields.datetime.now())
    year_by_month = fields.Datetime("Choose year", default=lambda self: fields.datetime.now())
    year = fields.Datetime("Choose year", default=lambda self: fields.datetime.now())

    @api.onchange('report_types')
    def _readonly_date(self):
        for record in self:
            #check day
            if record.report_types == "by_day":
                record.check_day = True
                record.check_month = False
                record.check_year = False
            else:
                record.check_day = False

            #check month
            if record.report_types == "by_month":
                record.check_month = True
                record.check_day = False
                record.check_year = False
            else:
                record.check_month = False

            #check year
            if record.report_types == "by_year":
                record.check_year = True
                record.check_day = False
                record.check_month = False
            else:
                record.check_year = False

    def action_report(self):
        data = self.read()[0]
        if data['report_types'] == 'by_day':
            date_add2 = data['day'] + timedelta(days=7)
            
            tickets = self.env['parking.ticket'].search([("check_out", "<=", date_add2), ("check_out", ">=", data['day'])])
            tickets2 = self.env['parking.ticket'].read_group([("check_out", "<=", date_add2), ("check_out", ">=", data['day'])], 
                fields=['parking_ticket_name'], groupby=['parking_lot_id']
            )

            ticket_name = []

            for record in tickets:
                
                ticket_name.append(record.parking_ticket_name)

            data = {
                'form_data': data,
                'tickets2': tickets2,
                'ticket_name': ticket_name,
                'model': 'parking.ticket'
            }  

        return self.env.ref('intern_exercise.action_open_revenue_xlsx').report_action(self, data=data)