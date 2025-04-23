import frappe
from frappe import _

def execute(filters=None):
    conditions, doc_type = get_conditions(filters)
    columns = get_columns(doc_type)
    data = get_data(conditions, filters, doc_type)
    return columns, data

def get_columns(doc_type):
    columns = [
        {"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
            {"label": _("Invoice No."), "fieldname": "name", "fieldtype": "Link", "options": doc_type, "width": 160},
        {"label": _("Party"), "fieldname": "party", "fieldtype": "Link", "options": "Customer" if doc_type == "Sales Invoice" else "Supplier", "width": 300},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 180},
        {"label": _("Paid Amount"), "fieldname": "paid_amount", "fieldtype": "Currency", "width": 180},
        {"label": _("Outstanding Amount"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 180},
    ]
    return columns

def get_data(conditions, filters, doc_type):
    data = frappe.db.sql(f"""
        SELECT 
            t.name,
            t.posting_date,
            t.status,
            t.grand_total,
            IFNULL(pe.paid_amount, 0) AS paid_amount,
            (t.grand_total - IFNULL(pe.paid_amount, 0)) AS outstanding_amount,
            t.{ "customer" if doc_type == "Sales Invoice" else "supplier"} AS party
        FROM `tab{doc_type}` t
        LEFT JOIN (
            SELECT 
                per.reference_name AS invoice,
                SUM(per.allocated_amount) AS paid_amount
            FROM `tabPayment Entry Reference` per
            JOIN `tabPayment Entry` pe ON per.parent = pe.name
            WHERE per.reference_doctype = '{doc_type}'
            AND pe.docstatus = 1
            GROUP BY per.reference_name
        ) pe ON t.name = pe.invoice
        WHERE t.docstatus = 1
        {conditions}
    """, filters, as_dict=1)
    return data

def get_conditions(filters):
    conditions = ""
    doc_type = "Sales Invoice" if filters.get("party_type") == "Customer" else "Purchase Invoice"

    if filters.get("party"): 
        conditions += f" and t.{ 'customer' if doc_type == 'Sales Invoice' else 'supplier' }=%(party)s"
    if filters.get("name"): 
        conditions += " and t.name=%(name)s"
    if filters.get("status"):
        if filters.get("status") == "Outstanding":
            conditions += " and t.status IN ('Unpaid', 'Partly Paid', 'Overdue')"
        else:
            conditions += " and t.status=%(status)s"
    if filters.get("from_date"): 
        conditions += " and t.posting_date >= %(from_date)s"
    if filters.get("to_date"): 
        conditions += " and t.posting_date <= %(to_date)s"

    return conditions, doc_type
