
import frappe
from frappe import _

def execute(filters=None):
        conditions = get_conditions(filters)
        columns = get_columns() 
        data = get_data(conditions,filters)
        return columns, data
def get_columns():
        columns= [
                {"label":_("Invoice No."),"fieldname":"name","fieldtype":"Link","options":"Purchase invoice","width":200},
                {"label":_("Date"),"fieldname":"posting_date","fieldtype":"data","width":100},
                {"label":_("Supplier"),"fieldname":"supplier","fieldtype":"Link","options":"Supplier","width":300},
                {"label":_("Status"),"fieldname":"status","fieldtype":"Data","width":100},
                {"label":_("Grand Total"),"fieldname":"grand_total","fieldtype":"Currency","width":200},
                {"label":_("Outstanding Amount"),"fieldname":"outstanding_amount","fieldtype":"Currency","width":200},
                ]
        return columns
def get_data(conditions,filters):
        data = frappe.db.sql("""
                SELECT DISTINCT
                                pi.name,
                                pi.supplier,
                                pi.posting_date,
                                pi.status,
                                pi.grand_total,
                                pi.outstanding_amount
                               
                        FROM
                        `tabPurchase Invoice` pi

                        WHERE
                                pi.docstatus = 1
                                {conditions}

                """.format(conditions=conditions), filters, as_dict=1)
        return data


       
def get_conditions(filters):
        conditions = ""
        if filters.get("supplier"): conditions += " and pi.supplier=%(supplier)s"
        if filters.get("name"): conditions += " and pi.name=%(name)s"
        if filters.get("status"): conditions += " and pi.status=%(status)s"
        if filters.from_date: conditions += " and posting_date >= %(from_date)s"
        if filters.to_date: conditions += " and posting_date <= %(to_date)s"
        
        return conditions