frappe.listview_settings["Timesheet Entry"] = {
    add_fields: ["status"],
	has_indicator_for_draft: 1,
	get_indicator: function (doc) {
		if (doc.status === "Open") {
			// Closed
			return [__("Open"), "orange", "status,=,Open"];
		} else if (doc.status === "Sent for Approval") {
			// on hold
			return [__("Sent for Approval"), "green", "status,=,Sent for Approval"];
		} else if (doc.status === "Approved") {
			return [__("Approved"), "green", "status,=,Approved"];
		} 
        else if (doc.status === "Rejected") {
			return [__("Rejected"), "red", "status,=,Rejected"];
		} 
        else if (doc.status === "Cancelled") {
			return [__("Cancelled"), "red", "status,=,Cancelled"];
		} 
	},
};
