from odoo import api, models

class ParkingTicketReport(models.AbstractModel):
    _name = "report.intern_exercise.parking_ticket_report"

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [("parking_lot_id", "in", docids)]
        tickets = self.env["parking.ticket"].search(domain)
        parking_lot = tickets.mapped("parking_lot_id")
        parking_lot_tickets = [
            (park,
             tickets.filtered(lambda ticket:
               ticket.parking_lot_id == park))
            for park in parking_lot
        ]
        docargs = {
            "parking_lot_tickets": parking_lot_tickets,
        }
        return docargs
