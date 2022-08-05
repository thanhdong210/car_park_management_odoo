from odoo import models
class ReportTicketXlsx(models.AbstractModel):
    _name = 'report.intern_exercise.report_action_ticket_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, tickets):
        print(tickets)
        for obj in tickets:
            report_name = obj.parking_ticket_name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, obj.parking_ticket_name, bold)