from odoo import models, fields
from datetime import datetime
from datetime import timedelta
import calendar

class ReportRevenueXlsx(models.AbstractModel):
    _name = 'report.intern_exercise.report_action_revenue_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, form_data):
        format_1 = workbook.add_format({'bold': True, 'align': 'center'})
        format_2 = workbook.add_format({'italic': True, 'align': 'center'})
        bold = workbook.add_format({'bold': True})
        bold_2 = workbook.add_format({'bold': True, 'align': 'center'})
        if form_data.report_types == 'by_day':
            sheet = workbook.add_worksheet("report xlsx")
            date_add2 = form_data.day + timedelta(days=7)
            date_add3 = datetime.strftime(fields.Datetime.context_timestamp(self, date_add2), "%Y-%m-%d")
            form_time_title = datetime.strftime(fields.Datetime.context_timestamp(self, form_data.day), "%Y-%m-%d")
            sheet.write(1, 7, "Revenue report form " + form_time_title + " to " + date_add3, format_1)
            
            tickets2 = self.env['parking.ticket'].read_group([("check_out", "<=", date_add2), ("check_out", ">=", form_data.day)], 
                fields=['parking_ticket_name'], groupby=['parking_lot_id']
            )
            print(tickets2)

            sheet.set_column('B:B', 30)
            sheet.set_column('E:E', 15)
            sheet.set_column('F:F', 20)
            sheet.set_column('G:G', 20)
            sheet.set_column('H:H', 20)
            sheet.set_column('I:I', 20)
            sheet.set_column('J:J', 20)
            sheet.set_column('K:K', 20)
            sheet.set_column('L:L', 20)
            sheet.set_column('M:M', 20)

            col = 3
            row_day = 2
            col_day = 5
            col_car_type = 4
            row_car_type = 4
            col_price = 5
            row_price = 4
            row_total_price = 3
            col_total_price = 5

            list_total_price = []

            total_revenue = 0
            for i in range(len(tickets2)):
                sheet.write(row_car_type - 1, col, str(tickets2[i]["parking_lot_id"][1]), bold)
                list_total_price = [0, 0, 0, 0, 0, 0, 0]
                for record in (self.env["parking.lot"].browse(tickets2[i]["parking_lot_id"][0]).parking_vehicle_id.vehicle):
                    sheet.write(row_car_type, col_car_type, str(record.parking_vehicle_name), bold)
                    print(str(tickets2[i]["parking_lot_id"][1]))
                    tickets = self.env['parking.ticket'].search([('parking_lot_id.parking_lot_name', '=', str(tickets2[i]["parking_lot_id"][1])), 
                        ("check_out", "<=", date_add2), ("check_out", ">=", (form_data.day - timedelta(days=1))), ("car_type_id_relate", "=", record.id)
                    ])
                    
                    form_data_time = form_data.day
                    for j in range(7):
                        price = 0
                        form_time = datetime.strftime(fields.Datetime.context_timestamp(self, form_data_time), "%Y-%m-%d")
                        for ticket in tickets:
                            time = datetime.strftime(fields.Datetime.context_timestamp(self, ticket.check_out), "%Y-%m-%d")
                            if time == form_time:
                                price += ticket.price
                                list_total_price[j] += ticket.price
                                total_revenue += ticket.price
                            sheet.write(row_price, col_price, str(price))
                        col_price += 1
                        form_data_time += timedelta(days=1)

                    row_car_type += 1
                    col_price = 5
                    row_price += 1

                col_total_price = 5
                for b in range(7):
                    sheet.write(row_total_price, col_total_price, str(list_total_price[b]), format_2)
                    col_total_price += 1

                row_car_type += 1
                row_price += 1
                row_total_price = row_car_type - 1

            sheet.merge_range(row_car_type + 1, col_car_type + 6, row_car_type + 1, col_car_type + 7, "In total " + str(total_revenue), bold_2)

            day_time_xlsx = form_data.day
            for i in range(7):
                form_time = datetime.strftime(fields.Datetime.context_timestamp(self, day_time_xlsx), "%Y-%m-%d")
                sheet.write(row_day, col_day, str(form_time), bold)
                day_time_xlsx += timedelta(days=1)
                col_day += 1

        elif form_data.report_types == 'by_month':
            sheet = workbook.add_worksheet("report xlsx")
            month_time = datetime.strftime(fields.Datetime.context_timestamp(self, form_data.month_by_month), "%m")
            year_time = datetime.strftime(fields.Datetime.context_timestamp(self, form_data.year_by_month), "%Y")

            month_time_xlsx = int(month_time)
            year_time_xlsx = int(year_time)

            sheet.write(1, 6, "Revenue report for month " + month_time + " year " + year_time, format_1)
            bold = workbook.add_format({'bold': True})

            col = 3
            row_day = 2
            col_day = 5
            col_car_type = 4
            row_car_type = 4
            col_price = 5
            row_price = 4
            row_total_price = 3
            col_total_price = 5

            sheet.set_column('E:E', 15)
            sheet.set_column('B:B', 15)

            tickets3 = self.env['parking.ticket'].read_group([], 
                fields=['parking_ticket_name'], groupby=['parking_lot_id']
            )

            calendar_month = calendar.monthcalendar(year_time_xlsx, month_time_xlsx)

            list_total_price= [0] * len(calendar.monthcalendar(year_time_xlsx, month_time_xlsx))
            total_revenue = 0

            for i in range(len(tickets3)):
                sheet.write(row_car_type - 1, col, str(tickets3[i]["parking_lot_id"][1]), bold)

                for g in range(len(calendar.monthcalendar(year_time_xlsx, month_time_xlsx))):
                    list_total_price[g] = 0

                for record in (self.env["parking.lot"].browse(tickets3[i]["parking_lot_id"][0]).parking_vehicle_id.vehicle):
                    sheet.write(row_car_type, col_car_type, str(record.parking_vehicle_name), bold)

                    tickets4 = self.env['parking.ticket'].search([
                        ('parking_lot_id.parking_lot_name', '=', str(tickets3[i]["parking_lot_id"][1])), 
                        ("car_type_id_relate", "=", record.id),
                        ("check_out", "!=", False)
                    ])
                    index = 0
                    for e in calendar_month:
                        price_list = 0
                        
                        for ticket in tickets4:
                            ticket_time_month = datetime.strftime(fields.Datetime.context_timestamp(self, ticket.check_out), "%m")
                            ticket_time_year = datetime.strftime(fields.Datetime.context_timestamp(self, ticket.check_out), "%Y")
                            
                            if ticket_time_month == month_time and ticket_time_year == year_time:
                                ticket_time_day = datetime.strftime(fields.Datetime.context_timestamp(self, ticket.check_out), "%d")
                                ticket_time_day2 = int(ticket_time_day)
                                for d in range(7):
                                    if ticket_time_day2 == e[d]:
                                        price_list += ticket.price
                        sheet.write(row_price, col_price, price_list)
                        list_total_price[index] += price_list
                        total_revenue += price_list
                        index += 1
                        col_price += 1

                    row_car_type += 1
                    col_price = 5
                    row_price += 1

                print(list_total_price)
                for h in range(len(calendar.monthcalendar(year_time_xlsx, month_time_xlsx))):
                    sheet.write(row_total_price, col_total_price, list_total_price[h], format_2)
                    col_total_price += 1

                row_car_type += 1
                row_price += 1
                col_total_price = 5
                row_total_price = row_car_type - 1

            week_len = len(calendar.monthcalendar(year_time_xlsx, month_time_xlsx))
            print(total_revenue)

            sheet.merge_range(row_car_type + 1, col_car_type + len(calendar.monthcalendar(year_time_xlsx, month_time_xlsx)) - 1, row_car_type + 1, col_car_type + 
            len(calendar.monthcalendar(year_time_xlsx, month_time_xlsx)), "In total: " + str(total_revenue), bold_2)

            for i in range(1, week_len + 1):
                sheet.write(row_day, col_day, "Week " + str(i), bold)
                col_day += 1

        elif form_data.report_types == 'by_year':
            sheet = workbook.add_worksheet("report xlsx")
            bold = workbook.add_format({'bold': True})
            year_time = datetime.strftime(fields.Datetime.context_timestamp(self, form_data.year), "%Y")
            sheet.write(1, 8, "Revenue report for year " + year_time, format_1)
            
            tickets_year = self.env['parking.ticket'].read_group([], 
                fields=['parking_ticket_name'], groupby=['parking_lot_id']
            )

            sheet.set_column('E:E', 15)

            col = 3
            row_month = 2
            col_month = 5
            col_car_type = 4
            row_car_type = 4
            col_price = 5
            row_price = 4
            row_total_price = 3
            col_total_price = 5

            list_total_price = []

            total_revenue = 0

            for a in range(len(tickets_year)):
                price_total_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                print(tickets_year[a]["parking_lot_id"][1])
                sheet.write(row_car_type - 1, col, str(tickets_year[a]["parking_lot_id"][1]), bold)
                for record in (self.env["parking.lot"].browse(tickets_year[a]["parking_lot_id"][0]).parking_vehicle_id.vehicle):
                    sheet.write(row_car_type, col_car_type, str(record.parking_vehicle_name), bold)

                    tickets_year_filter = self.env['parking.ticket'].search([
                        ('parking_lot_id.parking_lot_name', '=', str(tickets_year[a]["parking_lot_id"][1])), 
                        ("car_type_id_relate", "=", record.id),
                        ("check_out", "!=", False)
                    ])

                    price_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    

                    for ticket in tickets_year_filter:
                        ticket_time_year = datetime.strftime(fields.Datetime.context_timestamp(self, ticket.check_out), "%Y")
                        if ticket_time_year == year_time:
                            ticket_time_month = datetime.strftime(fields.Datetime.context_timestamp(self, ticket.check_out), "%m")
                            ticket_time_month2 = int(ticket_time_month)
                            if ticket_time_month2 == 1:
                                price_list[0] += ticket.price
                            elif ticket_time_month2 == 2:
                                price_list[1] += ticket.price
                            elif ticket_time_month2 == 3:
                                price_list[2] += ticket.price
                            elif ticket_time_month2 == 4:
                                price_list[3] += ticket.price
                            elif ticket_time_month2 == 5:
                                price_list[4] += ticket.price
                            elif ticket_time_month2 == 6:
                                price_list[5] += ticket.price
                            elif ticket_time_month2 == 7:
                                price_list[6] += ticket.price
                            elif ticket_time_month2 == 8:
                                price_list[7] += ticket.price
                            elif ticket_time_month2 == 9:
                                price_list[8] += ticket.price
                            elif ticket_time_month2 == 10:
                                price_list[9] += ticket.price
                            elif ticket_time_month2 == 11:
                                price_list[10] += ticket.price
                            elif ticket_time_month2 == 12:
                                price_list[11] += ticket.price

                    for c in range(12):
                        price_total_list[c] += price_list[c]
                        total_revenue += price_list[c]

                    for l in range(12):
                        sheet.write(row_price, col_price + l, price_list[l])

                    row_car_type += 1
                    col_price = 5
                    row_price += 1

                col_total_price = 5
                for d in range(12):
                    sheet.write(row_total_price, col_total_price, price_total_list[d])
                    col_total_price += 1

                row_car_type += 1
                row_price += 1
                row_total_price = row_car_type - 1
            
            month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

            sheet.merge_range(row_car_type + 1, col_car_type + 12, row_car_type + 1, col_car_type + 11, "In total " + str(total_revenue), bold_2)

            for k in range(12):
                sheet.write(row_month, col_month, month[k], bold)
                col_month += 1

        
        