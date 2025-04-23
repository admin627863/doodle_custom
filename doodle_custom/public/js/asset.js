frappe.ui.form.on('Asset', {

	refresh: function(frm) {
		frappe.ui.form.trigger("Asset", "is_existing_asset");
		frm.toggle_display("next_depreciation_date", frm.doc.docstatus < 1);
		frm.events.make_schedules_editable(frm);

		if (frm.doc.docstatus==1) {
			if (in_list(["Submitted", "Partially Depreciated", "Fully Depreciated"], frm.doc.status)) {
				frm.add_custom_button(__("Transfer Asset"), function() {
					erpnext.asset.transfer_asset(frm);
				}, __("Manage"));

				frm.add_custom_button(__("Scrap Asset Custom"), function() {
					erpnext.asset.scrap_asset(frm);
				}, __("Manage"));

				frm.add_custom_button(__("Sell Asset"), function() {
					frm.trigger("make_sales_invoice");
				}, __("Manage"));

			} else if (frm.doc.status=='Scrapped') {
				frm.add_custom_button(__("Restore Asset"), function() {
					erpnext.asset.restore_asset(frm);
				}, __("Manage"));
			}

			if (frm.doc.maintenance_required && !frm.doc.maintenance_schedule) {
				frm.add_custom_button(__("Maintain Asset"), function() {
					frm.trigger("create_asset_maintenance");
				}, __("Manage"));
			}

			frm.add_custom_button(__("Repair Asset"), function() {
				frm.trigger("create_asset_repair");
			}, __("Manage"));

			frm.add_custom_button(__("Split Asset"), function() {
				frm.trigger("split_asset");
			}, __("Manage"));

			if (frm.doc.status != 'Fully Depreciated') {
				frm.add_custom_button(__("Adjust Asset Value"), function() {
					frm.trigger("create_asset_value_adjustment");
				}, __("Manage"));
			}

			if (!frm.doc.calculate_depreciation) {
				frm.add_custom_button(__("Create Depreciation Entry"), function() {
					frm.trigger("make_journal_entry");
				}, __("Manage"));
			}

			if (frm.doc.purchase_receipt || !frm.doc.is_existing_asset) {
				frm.add_custom_button(__("View General Ledger"), function() {
					frappe.route_options = {
						"voucher_no": frm.doc.name,
						"from_date": frm.doc.available_for_use_date,
						"to_date": frm.doc.available_for_use_date,
						"company": frm.doc.company
					};
					frappe.set_route("query-report", "General Ledger");
				}, __("Manage"));
			}

			if (frm.doc.depr_entry_posting_status === "Failed") {
				frm.trigger("set_depr_posting_failure_alert");
			}

			frm.trigger("setup_chart");
		}

		frm.trigger("toggle_reference_doc");

		if (frm.doc.docstatus == 0) {
			frm.toggle_reqd("finance_books", frm.doc.calculate_depreciation);

			if (frm.doc.is_composite_asset && !frm.doc.capitalized_in) {
				$('.primary-action').prop('hidden', true);
				$('.form-message').text('Capitalize this asset to confirm');

				frm.add_custom_button(__("Capitalize Asset"), function() {
					frm.trigger("create_asset_capitalization");
				});
			}
		}
	},
});

erpnext.asset.scrap_asset = function(frm) {
	frappe.confirm(__("Do you really want to scrap this asset?"), function () {
		frappe.call({
			args: {
				"asset_name": frm.doc.name
			},
			method: "doodle_custom.doodle_custom.doctype.asset.depreciation.scrap_asset",
			callback: function(r) {
				cur_frm.reload_doc();
			}
		})
	})
};
erpnext.asset.restore_asset = function(frm) {
	frappe.confirm(__("Do you really want to restore this scrapped asset?"), function () {
		frappe.call({
			args: {
				"asset_name": frm.doc.name
			},
			method: "doodle_custom.doodle_custom.doctype.asset.depreciation.restore_asset",
			callback: function(r) {
				cur_frm.reload_doc();
			}
		})
	})
};


frappe.ui.form.on("Asset", {
    refresh: function (frm) {
        // Hide the "Scrap Asset" button from the Manage dropdown
        frm.remove_custom_button("Scrap Asset", "Manage");
    }
});