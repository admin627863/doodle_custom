// Copyright (c) 2025, Doodle Tech and contributors

frappe.provide("erpnext.utils");

frappe.query_reports["Statement of Accounts"] = {
	"filters": [
			{
				"fieldname": "party_type",
				"label": __("Party Type"),
				"fieldtype": "Select",
				"options": ["Customer", "Supplier"],
				"default": "Customer",
				"reqd": 1,
				"on_change": function() {
					let party_type = frappe.query_report.get_filter_value("party_type");
					let party_filter = frappe.query_report.get_filter("party");
					
					// Update options dynamically
					party_filter.df.options = (party_type === "Customer") ? "Customer" : "Supplier";
					party_filter.refresh();
					frappe.query_report.refresh();
				}
			},
			{
				"fieldname": "party",
				"label": __("Party"),
				"fieldtype": "Link",
				"options": "Customer",  // Default to Customer, will be updated dynamically
				"reqd": 1
			},
			
			{
				"fieldname": "name",
				"label": __("Invoice No."),
				"fieldtype": "Data"
			},
			{
				"fieldname": "from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"default": frappe.defaults.get_user_default("year_start_date"),
				"reqd": 1
			},
			{
				"fieldname": "to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"default": frappe.defaults.get_user_default("year_end_date"),
				"reqd": 1
			},
			{
				"fieldname": "status",
				"label": __("Status"),
				"fieldtype": "Select",
				"options": [
					{ "value": "", "label": __("All") },
					{ "value": "Paid", "label": __("Paid") },
					{ "value": "Unpaid", "label": __("Unpaid") },
					{ "value": "Partly Paid", "label": __("Partly Paid") },
					{ "value": "Overdue", "label": __("Overdue") },
					{ "value": "Outstanding", "label": __("Outstanding") }
				],
			}
		]
	};