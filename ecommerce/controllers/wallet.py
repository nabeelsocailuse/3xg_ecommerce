import frappe

from ecommerce.services.wallet_service import (
	adding,
	updating,
	getting,
	adding_transaction
)

@frappe.whitelist(allow_guest=True)
def add(**kwargs):
	return adding(kwargs)

@frappe.whitelist(allow_guest=True)
def update(**kwargs):
	return updating(kwargs)

@frappe.whitelist(allow_guest=True)
def get(**kwargs):
	return getting(kwargs)

@frappe.whitelist(allow_guest=True)
def add_transaction(**kwargs):
	return adding_transaction(kwargs)