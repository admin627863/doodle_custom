import frappe
from datetime import date, datetime, timedelta
from frappe.utils import date_diff, add_to_date, today
import string
import random

@frappe.whitelist()
def cron():
    today_date = datetime.now().date()
    
    # Fetch Maintenance Schedules
    maintenance_schedules = frappe.get_all("Maintenance Schedule", filters={"status": "Submitted"}, fields=["name", "custom_user"])

    print(maintenance_schedules)
    for schedule in maintenance_schedules:
        # Fetch schedules from child table
        schedules = frappe.get_all("Maintenance Schedule Detail", filters={"parent": schedule.name}, fields=["scheduled_date"])
        print(schedules)
        for schedule_date in schedules:
            # Convert schedule date to datetime object
            schedule_date_value = schedule_date.scheduled_date
            print(schedule_date_value)
            # # Calculate the difference between today's date and schedule date
            date_difference = (schedule_date_value - today_date).days
            print(date_difference)

            
            # # Check if the schedule date is before today's date
            if date_difference == 0:
                # Construct notification message
                message = f"Reminder: Maintenance schedule '{schedule.name}' is approaching on {schedule_date_value}. Please ensure necessary actions are taken."

                # Send notification email
                send_notification_email(schedule.custom_user, message)


@frappe.whitelist()
def send_notification_email(recipient, message):
    try:
        frappe.sendmail(
            recipients=recipient,
            subject=f"Reminder for Maintenance schedule",
            message=message
        )
        return "Email sent successfully"
    except Exception as e:
        frappe.log_error(f"Error sending email: {str(e)}")
        return "Failed to send email"

if __name__ == "__main__":
    cron()


@frappe.whitelist()
def daily():
    today_date = datetime.now().date()
    
    # Fetch Maintenance Schedules
    maintenance_schedules = frappe.get_all("Maintenance Schedule", filters={"status": "Submitted"}, fields=["name", "custom_user"])

    print(maintenance_schedules)
    for schedule in maintenance_schedules:
        # Fetch schedules from child table
        schedules = frappe.get_all("Maintenance Schedule Detail", filters={"parent": schedule.name}, fields=["scheduled_date"])
        print(schedules)
        for schedule_date in schedules:
            # Convert schedule date to datetime object
            schedule_date_value = schedule_date.scheduled_date
            print(schedule_date_value)
            # # Calculate the difference between today's date and schedule date
            date_difference = (schedule_date_value - today_date).days
            print(date_difference)

            
            # # Check if the schedule date is before today's date
            if date_difference == 0:
                # Construct notification message
                message = f"Reminder: Maintenance schedule '{schedule.name}' is approaching on {schedule_date_value}. Please ensure necessary actions are taken."

                # Send notification email
                send_notification_email_daily(schedule.custom_user, message)


@frappe.whitelist()
def send_notification_email_daily(recipient, message):
    try:
        frappe.sendmail(
            recipients=recipient,
            subject=f"Reminder for Maintenance schedule",
            message=message
        )
        return "Email sent successfully"
    except Exception as e:
        frappe.log_error(f"Error sending email: {str(e)}")
        return "Failed to send email"

if __name__ == "__main__":
    daily()



# @frappe.whitelist()
# def d_weekly():
#     sales_invoice = frappe.db.get_list(
#         'Sales Invoice',
#         fields=("name"),
#         filters={
#             "docstatus": 1,
#             "auto_repeat_frequency": "Weekly",
#             "enable_recurring": 1
#         },
#     )
#     print(sales_invoice)
#     for si in sales_invoice:
#         # print(si.name)

#         doc = frappe.get_doc('Sales Invoice', si.name)
#         doc.flags.ignore_permissions = True
#         # print(doc.name)
#         for i in doc.items:
#             # print(i.to_date)
#             # print(today())
#             current_date = str(today())
#             # print(current_date)
#             pre_date = str(i.to_date)
#             if pre_date == current_date:
#                 # if doc.auto_repeat_frequency == 'Daily':

#                 new_si = frappe.new_doc("Sales Invoice")
#                 # for i in doc.items:
#                 after_week = add_to_date(current_date, days=7, as_string=True)
#                 new_si.append("items", {
#                     'item_code': i.item_code,
#                     'item_name': i.item_name,
#                     'description': i.description,
#                     'from_date': current_date,
#                     'plan_frequency': i.plan_frequency,
#                     'to_date': after_week,
#                     'qty': i.qty,
#                     'rate': i.rate,
#                     'amount': i.amount,
#                     'uom': i.uom,
#                     'cost_center': i.cost_center
#                 })
#                 new_si.customer = doc.customer
#                 new_si.cost_center = doc.cost_center or ''
#                 new_si.enable_recurring = True
#                 new_si.customer_address = doc.customer_address or ''
#                 if doc.taxes_and_charges != '':
#                     new_si.taxes_and_charges = doc.taxes_and_charges or ''
#                     for tax in doc.taxes:
#                         new_si.append("taxes", {
#                             'charge_type': tax.charge_type,
#                             'account_head': tax.account_head,
#                             'description': tax.description,
#                             'cost_center': i.cost_center,
#                             'rate': tax.rate,
#                             'tax_amount': tax.tax_amount,
#                             'base_tax_amount': tax.base_tax_amount,
#                             'total': tax.base_tax_amount,
#                             'base_total': tax.base_tax_amount,
#                             'base_tax_amount_after_discount_amount': tax.base_tax_amount_after_discount_amount
#                         })

#                 new_si.po = doc.po or ''
#                 new_si.vat_no = doc.vat_no or ''
#                 new_si.auto_repeat_frequency = doc.auto_repeat_frequency
#                 new_si.flags.ignore_permissions = True
#                 new_si.save(ignore_permissions=True)
#                 frappe.db.commit()
#             else:
#                 pass


# @frappe.whitelist()
# def d_monthly():
#     sales_invoice = frappe.db.get_list(
#         'Sales Invoice',
#         fields=("name"),
#         filters={
#             "docstatus": 1,
#             "auto_repeat_frequency": "Monthly",
#             "enable_recurring": 1
#         },
#     )
#     print(sales_invoice)
#     for si in sales_invoice:
#         # print(si.name)

#         doc = frappe.get_doc('Sales Invoice', si.name)
#         doc.flags.ignore_permissions = True
#         # print(doc.name)
#         for i in doc.items:
#             # print(i.to_date)
#             # print(today())
#             current_date = str(today())
#             # print(current_date)
#             pre_date = str(i.to_date)
#             if pre_date == current_date:
#                 # if doc.auto_repeat_frequency == 'Daily':

#                 new_si = frappe.new_doc("Sales Invoice")
#                 # for i in doc.items:
#                 after_one_months = add_to_date(
#                     current_date, months=1, as_string=True)
#                 new_si.append("items", {
#                     'item_code': i.item_code,
#                     'item_name': i.item_name,
#                     'description': i.description,
#                     'from_date': current_date,
#                     'plan_frequency': i.plan_frequency,
#                     'to_date': after_one_months,
#                     'qty': i.qty,
#                     'rate': i.rate,
#                     'amount': i.amount,
#                     'uom': i.uom,
#                     'cost_center': i.cost_center
#                 })
#                 new_si.customer = doc.customer
#                 new_si.cost_center = doc.cost_center or ''
#                 new_si.enable_recurring = True
#                 new_si.customer_address = doc.customer_address or ''
#                 if doc.taxes_and_charges != '':
#                     new_si.taxes_and_charges = doc.taxes_and_charges or ''
#                     for tax in doc.taxes:
#                         new_si.append("taxes", {
#                             'charge_type': tax.charge_type,
#                             'account_head': tax.account_head,
#                             'description': tax.description,
#                             'cost_center': i.cost_center,
#                             'rate': tax.rate,
#                             'tax_amount': tax.tax_amount,
#                             'base_tax_amount': tax.base_tax_amount,
#                             'total': tax.base_tax_amount,
#                             'base_total': tax.base_tax_amount,
#                             'base_tax_amount_after_discount_amount': tax.base_tax_amount_after_discount_amount
#                         })
#                 new_si.po = doc.po or ''
#                 new_si.vat_no = doc.vat_no or ''
#                 new_si.auto_repeat_frequency = doc.auto_repeat_frequency
#                 new_si.flags.ignore_permissions = True
#                 new_si.save(ignore_permissions=True)
#                 frappe.db.commit()
#             else:
#                 pass


# @frappe.whitelist()
# def d_quarterly():
#     sales_invoice = frappe.db.get_list(
#         'Sales Invoice',
#         fields=("name"),
#         filters={
#             "docstatus": 1,
#             "auto_repeat_frequency": "Quarterly",
#             "enable_recurring": 1
#         },
#     )
#     # print(sales_invoice)
#     for si in sales_invoice:
#         # print(si.name)

#         doc = frappe.get_doc('Sales Invoice', si.name)
#         doc.flags.ignore_permissions = True
#         # print(doc.name)
#         for i in doc.items:
#             # print(i.to_date)
#             # print(today())
#             current_date = str(today())
#             # print(current_date)
#             pre_date = str(i.to_date)
#             if pre_date == current_date:
#                 # if doc.auto_repeat_frequency == 'Daily':

#                 new_si = frappe.new_doc("Sales Invoice")
#                 # for i in doc.items:
#                 after_three_months = add_to_date(
#                     current_date, months=3, as_string=True)
#                 new_si.append("items", {
#                     'item_code': i.item_code,
#                     'item_name': i.item_name,
#                     'description': i.description,
#                     'from_date': current_date,
#                     'plan_frequency': i.plan_frequency,
#                     'to_date': after_three_months,
#                     'qty': i.qty,
#                     'rate': i.rate,
#                     'amount': i.amount,
#                     'uom': i.uom,
#                     'cost_center': i.cost_center
#                 })
#                 new_si.customer = doc.customer
#                 new_si.cost_center = doc.cost_center or ''
#                 new_si.enable_recurring = True
#                 new_si.customer_address = doc.customer_address or ''
#                 if doc.taxes_and_charges != '':
#                     new_si.taxes_and_charges = doc.taxes_and_charges or ''
#                     for tax in doc.taxes:
#                         new_si.append("taxes", {
#                             'charge_type': tax.charge_type,
#                             'account_head': tax.account_head,
#                             'description': tax.description,
#                             'cost_center': i.cost_center,
#                             'rate': tax.rate,
#                             'tax_amount': tax.tax_amount,
#                             'base_tax_amount': tax.base_tax_amount,
#                             'total': tax.base_tax_amount,
#                             'base_total': tax.base_tax_amount,
#                             'base_tax_amount_after_discount_amount': tax.base_tax_amount_after_discount_amount
#                         })
#                 new_si.po = doc.po or ''
#                 new_si.vat_no = doc.vat_no or ''
#                 new_si.auto_repeat_frequency = doc.auto_repeat_frequency
#                 new_si.flags.ignore_permissions = True
#                 new_si.save(ignore_permissions=True)
#                 frappe.db.commit()
#             else:
#                 pass


# @frappe.whitelist()
# def d_half_year():
#     sales_invoice = frappe.db.get_list(
#         'Sales Invoice',
#         fields=("name"),
#         filters={
#             "docstatus": 1,
#             "auto_repeat_frequency": "Half-yearly",
#             "enable_recurring": 1
#         },
#     )
#     # print(sales_invoice)
#     for si in sales_invoice:
#         # print(si.name)

#         doc = frappe.get_doc('Sales Invoice', si.name)
#         doc.flags.ignore_permissions = True
#         # print(doc.name)
#         for i in doc.items:
#             # print(i.to_date)
#             # print(today())
#             current_date = str(today())
#             # print(current_date)
#             pre_date = str(i.to_date)
#             if pre_date == current_date:
#                 # if doc.auto_repeat_frequency == 'Daily':

#                 new_si = frappe.new_doc("Sales Invoice")
#                 # for i in doc.items:
#                 after_six_months = add_to_date(
#                     current_date, months=6, as_string=True)
#                 new_si.append("items", {
#                     'item_code': i.item_code,
#                     'item_name': i.item_name,
#                     'description': i.description,
#                     'from_date': current_date,
#                     'plan_frequency': i.plan_frequency,
#                     'to_date': after_six_months,
#                     'qty': i.qty,
#                     'rate': i.rate,
#                     'amount': i.amount,
#                     'uom': i.uom,
#                     'cost_center': i.cost_center
#                 })
#                 new_si.customer = doc.customer
#                 new_si.cost_center = doc.cost_center or ''
#                 new_si.enable_recurring = True
#                 new_si.customer_address = doc.customer_address or ''
#                 if doc.taxes_and_charges != '':
#                     new_si.taxes_and_charges = doc.taxes_and_charges or ''
#                     for tax in doc.taxes:
#                         new_si.append("taxes", {
#                             'charge_type': tax.charge_type,
#                             'account_head': tax.account_head,
#                             'description': tax.description,
#                             'cost_center': i.cost_center,
#                             'rate': tax.rate,
#                             'tax_amount': tax.tax_amount,
#                             'base_tax_amount': tax.base_tax_amount,
#                             'total': tax.base_tax_amount,
#                             'base_total': tax.base_tax_amount,
#                             'base_tax_amount_after_discount_amount': tax.base_tax_amount_after_discount_amount
#                         })
#                 new_si.po = doc.po or ''
#                 new_si.vat_no = doc.vat_no or ''
#                 new_si.auto_repeat_frequency = doc.auto_repeat_frequency
#                 new_si.flags.ignore_permissions = True
#                 new_si.save(ignore_permissions=True)
#                 frappe.db.commit()
#             else:
#                 pass


# @frappe.whitelist()
# def d_yearly():
#     sales_invoice = frappe.db.get_list(
#         'Sales Invoice',
#         fields=("name"),
#         filters={
#             "docstatus": 1,
#             "auto_repeat_frequency": "Yearly",
#             "enable_recurring": 1
#         },
#     )
#     # print(sales_invoice)
#     for si in sales_invoice:
#         # print(si.name)

#         doc = frappe.get_doc('Sales Invoice', si.name)
#         doc.flags.ignore_permissions = True
#         # print(doc.name)
#         for i in doc.items:
#             # print(i.to_date)
#             # print(today())
#             current_date = str(today())
#             # print(current_date)
#             pre_date = str(i.to_date)
#             if pre_date == current_date:
#                 # if doc.auto_repeat_frequency == 'Daily':

#                 new_si = frappe.new_doc("Sales Invoice")
#                 # for i in doc.items:
#                 after_one_year = add_to_date(
#                     current_date, months=12, as_string=True)
#                 new_si.append("items", {
#                     'item_code': i.item_code,
#                     'item_name': i.item_name,
#                     'description': i.description,
#                     'from_date': current_date,
#                     'plan_frequency': i.plan_frequency,
#                     'to_date': after_one_year,
#                     'qty': i.qty,
#                     'rate': i.rate,
#                     'amount': i.amount,
#                     'uom': i.uom,
#                     'cost_center': i.cost_center
#                 })
#                 new_si.customer = doc.customer
#                 new_si.cost_center = doc.cost_center or ''
#                 new_si.enable_recurring = True
#                 new_si.customer_address = doc.customer_address or ''
#                 if doc.taxes_and_charges != '':
#                     new_si.taxes_and_charges = doc.taxes_and_charges or ''
#                     for tax in doc.taxes:
#                         new_si.append("taxes", {
#                             'charge_type': tax.charge_type,
#                             'account_head': tax.account_head,
#                             'description': tax.description,
#                             'cost_center': i.cost_center,
#                             'rate': tax.rate,
#                             'tax_amount': tax.tax_amount,
#                             'base_tax_amount': tax.base_tax_amount,
#                             'total': tax.base_tax_amount,
#                             'base_total': tax.base_tax_amount,
#                             'base_tax_amount_after_discount_amount': tax.base_tax_amount_after_discount_amount
#                         })
#                 new_si.po = doc.po or ''
#                 new_si.vat_no = doc.vat_no or ''
#                 new_si.auto_repeat_frequency = doc.auto_repeat_frequency
#                 new_si.flags.ignore_permissions = True
#                 new_si.save(ignore_permissions=True)
#                 frappe.db.commit()
#             else:
#                 pass
