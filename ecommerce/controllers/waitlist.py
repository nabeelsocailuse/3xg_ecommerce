import frappe

from ecommerce.services.waitlist_service import (
	joining
)

@frappe.whitelist(allow_guest=True)
def join(**kwargs):
	return joining(kwargs)