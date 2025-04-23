import frappe


@frappe.whitelist()
def opportunity_comment(doc, handler=""):
    comment = frappe.db.get_list(
        'Comment',
        fields=("name"),
        filters={
            "reference_name":doc.party_name
        },
    )
    for i in comment:
        cm = frappe.get_doc('Comment', i.name)
        cm.flags.ignore_permissions = True
        if cm.comment_type == 'Comment':
            cmt = frappe.new_doc("Comment")
            cmt.comment_type = "Comment"
            cmt.reference_doctype = doc.doctype
            cmt.reference_name = doc.name
            cmt.comment_email = cm.comment_email
            cmt.comment_by = cm.comment_by
            cmt.content = cm.content
            cmt.flags.ignore_permissions  = True
            cmt.save()
            
    