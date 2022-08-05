from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class BatchUpdateWizard(models.TransientModel):
    _name = "report.parking.lot.wizard"
    _description = "Report parking lot"

    parking_lot_name = fields.Char('Parking lot name', required=True)
    working_time_from = fields.Float("Working time from", required=True)
    working_time_to = fields.Float("Working time to", required=True)

    def multi_update(self):
        ids = self.env.context['active_ids'] # selected record ids
        my_pets = self.env["parking.lot"].browse(ids)
        new_data = {}
        
        if self.parking_lot_name:
            new_data["parking_lot_name"] = self.parking_lot_name
        if self.working_time_from:
            new_data["working_time_from"] = self.working_time_from
        if self.working_time_to:
            new_data["working_time_to"] = self.working_time_to
        
        my_pets.write(new_data)  