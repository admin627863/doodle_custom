import frappe
from frappe import _
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.email.inbox import link_communication_to_document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import comma_and, cstr, getdate, has_gravatar, nowdate, validate_email_address

from erpnext.crm.doctype.lead.lead import Lead


class CustomLead(Lead):

    def validate(self):
        self.set_lead_name()
        self.set_title()
        self.set_status()
        # self.check_email_id_is_unique()
        self.validate_email_id()
        # self.validate_contact_date()
        # self.set_prev()