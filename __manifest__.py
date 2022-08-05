{
    'name': "Parking manage",
    'summary': "Parking manage",
    'description': "Manage car parking in parking lot",
    'author': "Thanh Dong",
    'website': "None",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'report_xlsx'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/lot_vehicle_relation.xml',
        'views/parking_vehicle.xml',
        'views/parking_ticket.xml',
        'views/parking_pricelist.xml',
        'views/parking_pricelist_item.xml',
        'views/check_out_action_popup.xml',

        'wizard/report_parking_lot.xml',
        'wizard/report_parking_ticket.xml',
        'wizard/report_revenue_by_car_type_wizard.xml',
        'wizard/report_revenue_by_lot_wizard.xml',
        'wizard/report_revenue_wizard.xml',

        'report/reports.xml',
        'report/total_car_now.xml',
        'report/parking_ticket_report.xml', 
        'report/parking_ticket_report_wizard.xml',
        'report/report_revenue_by_car_type.xml',
        'report/report_revenue_by_lot.xml',

        'views/parking_lot.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}