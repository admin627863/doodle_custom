import frappe
from frappe import _

@frappe.whitelist(allow_guest=False)
def get_all_leads():
    """
    API to fetch all Lead records with selected fields.
    Example:
        /api/method/your_app.api.get_all_leads
    """

    # Fetch all leads (you can add filters as needed)
    leads = frappe.get_all(
        "Lead",
        fields=[
            "name as lead_id",
            "company",
            "creation",
            "department",
            "email_id",
            "first_name",
            "last_name",
            "phone",
            "source",
            "status"
        ],
        order_by="creation desc"
    )

    if not leads:
        return {"success": False, "message": "No leads found."}

    # Structure API response
    return {
        "success": True,
        "total_leads": len(leads),
        "data": leads
    }