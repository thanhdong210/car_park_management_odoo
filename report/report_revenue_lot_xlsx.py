from odoo import models
class ReportTicketXlsx(models.AbstractModel):
    _name = 'report.intern_exercise.report_action_revenue_lot_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, form):
        report_name = "Report revenue by lot"
        sheet = workbook.add_worksheet(report_name)
        bold = workbook.add_format({'bold': True})
        sheet.set_column('A:A', 12)
        sheet.set_column('B:B', 12)
        sheet.write(0, 0, report_name, bold)
        sheet.write(1, 0, form.parking_lot_name_id_relate, bold)
        sheet.write(1, 1, str(data['price']) + "vnd", bold)