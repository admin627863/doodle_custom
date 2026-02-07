import frappe

def execute(filters=None):
    conditions = []
    if filters.get("custom_services"):
        conditions.append("o.custom_services = %(custom_services)s")
    if filters.get("last_updated_by"):
        conditions.append("o.modified_by = %(last_updated_by)s")
    if filters.get("status"):
        conditions.append("o.status = %(status)s")

    where_clause = "WHERE o.docstatus < 2"
    if conditions:
        where_clause += " AND " + " AND ".join(conditions)

    columns = [
        {"label": "Opportunity", "fieldname": "name", "fieldtype": "Link", "options": "Opportunity", "width": 150},
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Custom Services", "fieldname": "custom_services", "fieldtype": "Data", "width": 180},
        {"label": "Opportunity Owner", "fieldname": "owner", "fieldtype": "Link", "options": "User", "width": 180},
        {"label": "Last Updated By", "fieldname": "modified_by", "fieldtype": "Link", "options": "User", "width": 180},
        {"label": "Last Updated On", "fieldname": "modified", "fieldtype": "Datetime", "width": 160},
        {"label": "Latest Note", "fieldname": "latest_note", "fieldtype": "Data", "width": 300},
    ]

    data = frappe.db.sql(f"""
        SELECT
            o.name,
            o.customer_name,
            o.status,
            o.custom_services,
            o.owner,
            o.modified_by,
            o.modified,
            (
                SELECT cn.note
                FROM `tabCRM Note` cn
                WHERE cn.parent = o.name
                ORDER BY cn.idx DESC
                LIMIT 1
            ) AS latest_note
        FROM `tabOpportunity` o
        {where_clause}
        ORDER BY o.modified DESC
    """, filters, as_dict=True)

    return columns, data
