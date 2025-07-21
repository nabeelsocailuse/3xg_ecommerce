import frappe

from ecommerce.services.bankaccount_service import (
	add_bank_account,
	get_bank_account
)

# https://zirconstage.3xg.africa/api/method/ecommerce.controllers.bankaccount.add
@frappe.whitelist(allow_guest=True)
def add(**kwargs):
	return add_bank_account(kwargs)

# https://zirconstage.3xg.africa/api/method/ecommerce.controllers.bankaccount.get
@frappe.whitelist(allow_guest=True)
def get(**kwargs):
	return get_bank_account(kwargs)
