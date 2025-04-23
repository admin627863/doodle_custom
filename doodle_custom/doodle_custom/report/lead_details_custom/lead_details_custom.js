// Copyright (c) 2023, Doodle Tech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lead Details Custom"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			options: [
				{ "value": "Lead", "label": __("Lead") },
				{ "value": "Open", "label": __("Open") },
				{ "value": "Replied", "label": __("Replied") },
				{ "value": "Quote Sent", "label": __("Quote Sent") },
				{ "value": "Quote Sent-Interested", "label": __("Quote Sent-Interested") },
				{ "value": "Quote Sent-No response", "label": __("Quote Sent-No response") },
				{ "value": "Opportunity", "label": __("Opportunity") },
				{ "value": "Quotation", "label": __("Quotation") },
				{ "value": "Lost Quote", "label": __("Lost Quote") },
				{ "value": "Converted", "label": __("Converted") },
				{ "value": "No Response-Close", "label": __("No Response-Close") },
				{ "value": "Do Not Contact", "label": __("Do Not Contact") },
			],
		},
		{
			"fieldname":"division",
			"label": __("Division"),
			"fieldtype": "Link",
			"options": "Cost Center",
		},
		{
			"fieldname":"territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"options": "Territory",
		}

	]
};
