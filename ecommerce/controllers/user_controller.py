import frappe

from ecommerce.services.user_service import (
	list_users,
	creating_user,
	updating_user,
	verifying_user
)

@frappe.whitelist(allow_guest=True)
def list_user():
	return list_users() 

@frappe.whitelist(allow_guest=True)
def add_user(**kwargs):
	return creating_user(kwargs)

@frappe.whitelist(allow_guest=True)
def update_user(**kwargs):
	return updating_user(kwargs)

@frappe.whitelist(allow_guest=True)
def verify_user(**kwargs):
	return verifying_user(kwargs)