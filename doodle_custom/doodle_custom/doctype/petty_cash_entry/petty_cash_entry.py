# Copyright (c) 2023, Doodle Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Pettycashentry(Document):

    def on_submit(self):
        jv = frappe.new_doc("Journal Entry")
        jv.voucher_type = "Cash Entry"
        jv.posting_date = self.posting_date
        jv.user_remark = self.reference or ""
        jv.append("accounts", {
            'account': self.expense_account,
            'debit_in_account_currency': self.total_tax,
            'cost_center': self.division
        })
        jv.append("accounts", {
            'account': "Petty Cash - Others - DTL",
            'credit_in_account_currency': self.total_tax,
            'cost_center': self.division
        })
        jv.flags.ignore_permissions = True
        jv.submit()
