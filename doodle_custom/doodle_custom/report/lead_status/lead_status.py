import frappe

def execute(filters=None):
    conditions = []
    if filters.get("source"):
        conditions.append("l.source = %(source)s")
    if filters.get("last_updated_by"):
        conditions.append("l.modified_by = %(last_updated_by)s")
    if filters.get("status"):
        conditions.append("l.status = %(status)s")
    if filters.get("custom_services"):
        conditions.append("l.custom_services = %(custom_services)s")

    where_clause = "WHERE l.docstatus < 2"
    if conditions:
        where_clause += " AND " + " AND ".join(conditions)

    columns = [
        {"label": "Lead", "fieldname": "name", "fieldtype": "Link", "options": "Lead", "width": 150},
        {"label": "Lead Name", "fieldname": "lead_name", "fieldtype": "Data", "width": 200},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Source", "fieldname": "source", "fieldtype": "Data", "width": 180},
        {"label": "Custom Services", "fieldname": "custom_services", "fieldtype": "Data", "width": 180},
        {"label": "Lead Owner", "fieldname": "owner", "fieldtype": "Link", "options": "User", "width": 180},
        {"label": "Last Updated By", "fieldname": "modified_by", "fieldtype": "Link", "options": "User", "width": 180},
        {"label": "Last Updated On", "fieldname": "modified", "fieldtype": "Datetime", "width": 160},
        {"label": "Latest Note", "fieldname": "latest_note", "fieldtype": "Data", "width": 300},
    ]

    data = frappe.db.sql(f"""
        SELECT
            l.name,
            l.lead_name,
            l.status,
            l.source,
            l.custom_services,
            l.owner,
            l.modified_by,
            l.modified,
            (
                SELECT cn.note
                FROM `tabCRM Note` cn
                WHERE cn.parent = l.name
                ORDER BY cn.idx DESC
                LIMIT 1
            ) AS latest_note
        FROM `tabLead` l
        {where_clause}
        ORDER BY l.modified DESC
    """, filters, as_dict=True)

    return columns, data
