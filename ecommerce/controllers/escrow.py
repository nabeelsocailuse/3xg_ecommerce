import frappe

from ecommerce.services.escrow_service import (
	adding,
	updating
)

@frappe.whitelist(allow_guest=True)
def add(**kwargs):
	return adding(kwargs)

@frappe.whitelist(allow_guest=True)
def update(**kwargs):
	return updating(kwargs)