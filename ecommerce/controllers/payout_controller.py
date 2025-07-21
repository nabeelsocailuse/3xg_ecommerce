import frappe

from ecommerce.services.payout_service import (
	add_payout_request
)

@frappe.whitelist(allow_guest=True)
def add(**kwargs):
    return add_payout_request(kwargs)