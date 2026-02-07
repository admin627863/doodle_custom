import frappe

def validate_delivery_note(doc, method):
    """
    Enforces that Delivery Note must have a Sales Order 
    only if the cost center contains 'dooprint - dtl'.
    """
    # Check if the cost center contains 'dooprint - dtl'
    # if doc.cost_center and "dooprint - dtl" in doc.cost_center.lower():
    if doc.cost_center and any(keyword in doc.cost_center.lower() for keyword in ["dooprint - dtl", "dooprint - dtld"]):
        # If it does, skip validation
        return
    
    # If cost center is not 'dooprint - dtl', enforce the Sales Order check
    if not any(item.against_sales_order for item in doc.items):
        frappe.throw("Sales Order is required for Delivery Note.")
