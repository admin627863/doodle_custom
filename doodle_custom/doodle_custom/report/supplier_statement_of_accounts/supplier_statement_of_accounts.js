// Copyright (c) 2024, Doodle Tech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supplier Statement of Accounts"] = {
	"filters": [

		{
			"fieldname":"supplier",
			"label": __("Suplier"),
			"fieldtype": "Link",
			"options": "Supplier"
	},
	{
		"fieldname":"name",
		"label": __("No."),
		"fieldtype": "Link",
		"options": "Purchase Invoice"
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
			{ "value": "Paid", "label": __("Paid") },
			{ "value": "Unpaid", "label": __("Unpaid") },
			{ "value": "Partly Paid", "label": __("Partly Paid") },
			{ "value": "Overdue", "label": __("Overdue") }

		],
	},
	]
};
