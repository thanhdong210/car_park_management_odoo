from odoo import api, fields, models, tools, _

class ParkingTicket(models.Model):
    _name = "checkout.action"
    _description = "Check out ticket"
    _rec_name = 'price'

    
    total_time = fields.Char("Total time")
    price = fields.Float("Price")
    

    
    



    

    


    


