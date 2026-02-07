# your_app/your_app/tasks/cleanup.py
import urllib.request
import urllib.error
import frappe
from frappe.utils import now_datetime

CLEANUP_URL = "https://doodletech.ae/wp-content/plugins/cf7-data-api-sender/db-cleanup.php?key=doo-clean-db-25"
REQUEST_TIMEOUT = 30

def call_cleanup_endpoint():
    try:
        req = urllib.request.Request(CLEANUP_URL, headers={"User-Agent": "erpnext-cleanup-bot/1.0"})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            status = resp.getcode()
            body = resp.read(4096).decode("utf-8", errors="replace")
            frappe.log_error(title="Daily DB Cleanup Called",
                             message=f"Status: {status}\nTime: {now_datetime()}\nResponse: {body[:2000]}")
    except urllib.error.HTTPError as he:
        err_body = he.read().decode("utf-8", errors="replace") if hasattr(he, "read") else ""
        frappe.log_error(title="Daily DB Cleanup HTTPError",
                         message=f"HTTPError: {getattr(he,'code','')} {getattr(he,'reason','')}\nResponse: {err_body[:2000]}")
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Daily DB Cleanup Failed")