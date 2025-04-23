# Copyright (c) 2024, Doodle Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TimesheetEntry(Document):
	

		def on_submit(self):
				if self.status == "Approved":
						for i in self.time_and_attendace:
								timesheet = frappe.new_doc('Timesheet')
								timesheet.employee = self.employee
								timesheet.custom_parent_timesheet = self.name
							# Create a new timesheet detail for each item in the stock entry
								timesheet.append('time_logs', {
								'activity_type': i.activity_type,  # Assuming you have an activity type named 'Task'
								'from_time': i.from_time,  # Set your desired start time
								'to_time': i.to_time,    # Set your desired end time
								'hours': i.hours,            # Assuming 8 hours per day for each entry, adjust accordingly
								'is_billable': 1,         # Assuming all entries are billable, change if necessary
								'completed': 1,
								})

								timesheet.flags.ignore_permissions = True
								timesheet.submit()
								frappe.msgprint("Timesheet Created..")
  
@frappe.whitelist(allow_guest=True)
def update_status(s_name):
		frappe.db.sql("""update `tabTimesheet Entry` set status = "Sent for Approval" where name = %s""",(s_name))
		frappe.db.commit()
		frappe.reload_doc()
		frappe.msgprint("Status updated...")
