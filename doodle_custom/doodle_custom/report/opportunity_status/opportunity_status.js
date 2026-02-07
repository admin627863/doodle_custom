frappe.query_reports["Opportunity Status"] = {
    "filters": [
        {
            fieldname: "custom_services",
            label: "Custom Services",
            fieldtype: "Select",
            options: [
                "",
                "Printer",
                "AMC",
                "IT Infrastructure",
                "Modern Security",
                "ELV Solutions",
                "Enterprise Software",
                "Web Development & Branding",
                "Digital Marketing",
                "Cloud Services",
                "Email Solutions",
                "CCTV",
                "Others"
            ]
        },
        {
            fieldname: "last_updated_by",
            label: "Last Updated By",
            fieldtype: "Link",
            options: "User"
        },
        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: "\nOpen\nQuotation\nLost\nConverted",
            default: ""
        }
    ]
};
