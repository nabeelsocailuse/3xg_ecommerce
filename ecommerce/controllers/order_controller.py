
import frappe

from ecommerce.services.order_service import (
	list_orders, 
	delete_order, 
	get_single_order, 
	list_orders_by_merchant, 
	update_payment,
	creating_order,
	updating_order,
	order_return_request,
	update_order_status
)

@frappe.whitelist(allow_guest=True)
def get_orders(user_id):
	return list_orders(user_id)

@frappe.whitelist(allow_guest=True)
def get_orders_by_merchant(merchant_id):
	return list_orders_by_merchant(merchant_id)

@frappe.whitelist(allow_guest=True)
def get_order(user_id, order_id):
	return get_single_order(user_id, order_id)

@frappe.whitelist(allow_guest=True)
def get_ordersss(user_id, order_id):
	return "Hello World!!!!!!!!!!!!!!"

@frappe.whitelist(allow_guest=True)
def create_new_order(**kwargs):
	return creating_order(kwargs)

@frappe.whitelist(allow_guest=True)
def modify_order(**kwargs):
	return updating_order(kwargs)

@frappe.whitelist(allow_guest=True)
def update_status(order_id, new_status):
	return update_order_status(order_id, new_status)

@frappe.whitelist(allow_guest=True)
def remove_order(user_id, order_id):
	 return delete_order(user_id, order_id)

@frappe.whitelist(allow_guest=True)
def update_payment_status(user_id, order_id):
	 return update_payment(user_id, order_id)

@frappe.whitelist(allow_guest=True)
def return_request(**kwargs):
	return order_return_request(kwargs)