// Copyright (c) 2025, Doodle Tech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Division Specific Statement of Accounts"] = {
	"filters": [
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
	},
	{
		"fieldname":"name",
		"label": __("No."),
		"fieldtype": "Link",
		"options": "Sales Invoice"
	},
	{
		"fieldname": "cost_center",
		"label": __("Division"),
		"fieldtype": "Link",
		"options": "Cost Center"
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
		"fieldname":"status",
		"label": __("Status"),
		"fieldtype": "Select",
		options: [
			{ "value": "", "label": __("All") },
			{ "value": "Paid", "label": __("Paid") },
			{ "value": "Unpaid", "label": __("Unpaid") },
			{ "value": "Partly Paid", "label": __("Partly Paid") },
			{ "value": "Overdue", "label": __("Overdue") },
			{ "value": "Outstanding", "label": __("Outstanding") }
		],
	},
   


],
};
