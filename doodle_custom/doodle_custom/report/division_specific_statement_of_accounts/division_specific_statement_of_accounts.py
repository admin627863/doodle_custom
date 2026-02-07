
import frappe
from frappe import _

def execute(filters=None):
        conditions = get_conditions(filters)
        columns = get_columns() 
        data = get_data(conditions,filters)
        return columns, data
def get_columns():
        columns= [
                {"label":_("Invoice No."),"fieldname":"name","fieldtype":"Link","options":"Sales invoice","width": 200},
                {"label":_("Date"),"fieldname":"posting_date","fieldtype":"data","width": 100},
                {"label":_("Customer"),"fieldname":"customer","fieldtype":"Link","options":"Customer","width": 300},
				{"label": _("Division"), "fieldname": "cost_center", "fieldtype": "Link", "options": "Cost Center", "width": 200},
                {"label":_("Status"),"fieldname":"status","fieldtype":"Data","width": 100},
                {"label":_("Grand Total"),"fieldname":"grand_total","fieldtype":"Currency","width": 200},
                {"label":_("Outstanding Amount"),"fieldname":"outstanding_amount","fieldtype":"Currency","width": 200},
                ]
        return columns
def get_data(conditions,filters):
        data = frappe.db.sql("""
                SELECT DISTINCT
                                si.name,
                                si.customer,
                                si.posting_date,
                                si.status,
                                si.grand_total,
                                si.outstanding_amount,
                             	si.cost_center
                               
                        FROM
                        `tabSales Invoice` si

                        WHERE
                                si.docstatus = 1
                                {conditions}

                """.format(conditions=conditions), filters, as_dict=1)
        return data


       
def get_conditions(filters):
        conditions = ""
        if filters.get("customer"): conditions += " and si.customer=%(customer)s"
        if filters.get("name"): conditions += " and si.name=%(name)s"
        if filters.get("status"):
                if filters.get("status") != "":
                        if filters.get("status") == "Outstanding":
                                conditions += " and si.status IN ('Unpaid', 'Partly Paid', 'Overdue')"
                        else :
                                conditions += " and si.status=%(status)s"
        # if filters.get("status"): conditions += " and si.status=%(status)s"
        if filters.from_date: conditions += " and posting_date >= %(from_date)s"
        if filters.to_date: conditions += " and posting_date <= %(to_date)s"
        if filters.get("cost_center"): conditions += " and si.cost_center = %(cost_center)s"

        
        return conditions