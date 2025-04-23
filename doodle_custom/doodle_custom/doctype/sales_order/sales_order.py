import json

import frappe
import frappe.utils
from frappe.utils import cint, flt
from frappe import _, qb
from frappe.contacts.doctype.address.address import get_company_address
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.query_builder.functions import Sum
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html

from erpnext.accounts.doctype.sales_invoice.sales_invoice import (
	unlink_inter_company_doc,
	update_linked_doc,
	validate_inter_company_party,
)
from erpnext.accounts.party import get_party_account
from erpnext.controllers.selling_controller import SellingController
from erpnext.manufacturing.doctype.blanket_order.blanket_order import (
	validate_against_blanket_order,
)
from erpnext.manufacturing.doctype.production_plan.production_plan import (
	get_items_for_material_requests,
)
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.get_item_details import get_default_bom, get_price_list_rate
from erpnext.stock.stock_balance import get_reserved_qty, update_bin_qty
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

form_grid_templates = {"items": "templates/form_grid/item_grid.html"}

class CustomSalesOrder(SalesOrder):
    
    def validate(self):
            super(SalesOrder, self).validate()
            self.validate_delivery_date()
            self.validate_proj_cust()
            self.validate_po()
            self.validate_uom_is_integer("stock_uom", "stock_qty")
            self.validate_uom_is_integer("uom", "qty")
            self.validate_for_items()
            self.validate_warehouse()
            self.validate_drop_ship()
            self.validate_serial_no_based_delivery()
            validate_against_blanket_order(self)
            validate_inter_company_party(
                self.doctype, self.customer, self.company, self.inter_company_order_reference
            )

            if self.coupon_code:
                from erpnext.accounts.doctype.pricing_rule.utils import validate_coupon_code

                validate_coupon_code(self.coupon_code)

            from erpnext.stock.doctype.packed_item.packed_item import make_packing_list

            make_packing_list(self)

            self.validate_with_previous_doc()
            self.set_status()

            if not self.billing_status:
                self.billing_status = "Not Billed"
            if not self.delivery_status:
                self.delivery_status = "Not Delivered"

            self.reset_default_field_value("set_warehouse", "items", "warehouse")
    
    def on_submit(self):
            self.update_reserved_qty()

            frappe.get_doc("Authorization Control").validate_approving_authority(
                self.doctype, self.company, self.base_grand_total, self
            )
            self.update_project()
            self.update_prevdoc_status("submit")

            self.update_blanket_order()

            update_linked_doc(self.doctype, self.name, self.inter_company_order_reference)
            if self.coupon_code:
                from erpnext.accounts.doctype.pricing_rule.utils import update_coupon_code_count

                update_coupon_code_count(self.coupon_code, "used")
                
    
@frappe.whitelist(allow_guest=True)           
def check_credit_limit(customer, company, grand_total):
    # Convert grand_total to float to ensure it's a numeric value
    grand_total = flt(grand_total)

    # Fetch credit limit bypass option from Customer Credit Limit
    bypass_credit_limit_check = frappe.db.get_value(
        "Customer Credit Limit",
        {"parent": customer, "parenttype": "Customer", "company": company},
        "bypass_credit_limit_check"
    )

    # If bypass credit limit is enabled, skip the check
    if cint(bypass_credit_limit_check):
        return False  # No credit limit exceeded (bypass credit limit check)

    # Fetch credit limit for customer
    credit_limit = frappe.db.get_value(
        "Customer Credit Limit",
        {"parent": customer, "parenttype": "Customer", "company": company},
        "credit_limit"
    )

    # If there's no credit limit set, do not validate
    if not credit_limit:
        return False

    # Calculate outstanding amount for the customer (set to 0 if None)
    outstanding_amount = flt(get_customer_outstanding(customer, company))

    # Check if grand total exceeds credit limit
    total_amount = outstanding_amount + grand_total
    if total_amount > flt(credit_limit):
        return True  # Credit limit exceeded
    return False  # Credit limit not exceeded

def get_customer_outstanding(customer, company):
    """Fetches the outstanding amount for the customer"""
    outstanding_invoices = frappe.db.sql("""
        SELECT SUM(outstanding_amount) AS total_outstanding
        FROM `tabSales Invoice`
        WHERE customer = %s AND company = %s AND docstatus = 1 AND status != 'Paid'
    """, (customer, company), as_dict=True)

    # Return the outstanding amount, or 0 if no outstanding invoices found
    if outstanding_invoices and outstanding_invoices[0].get('total_outstanding') is not None:
        return outstanding_invoices[0].get('total_outstanding', 0)
    return 0  # If no outstanding invoices, return 0