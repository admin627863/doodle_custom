frappe.query_reports["Customer Statement of Accounts"] = {
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
