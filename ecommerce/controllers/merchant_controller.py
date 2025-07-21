import frappe

from ecommerce.services.merchant_service import (
    get_merchants, 
    get_merchant_by_id, 
    add_new_merchant, 
    calculate_merchant_performance,
get_merchant_balances
)

@frappe.whitelist(allow_guest=True)
def list_merchant():
    return get_merchants() 


@frappe.whitelist(allow_guest=True)
def get_merchant(merchant_id):
    return get_merchant_by_id(merchant_id)


@frappe.whitelist(allow_guest=True)
def add_merchant(merchant_id, username, email, password, phone, business_name, business_type, business_category, business_address, business_location_lat, business_location_long, first_name, last_name,  role=None, street=None, city=None, state=None, country=None):
    return add_new_merchant(merchant_id, username, email, password, phone, business_name, business_type, business_category, business_address, business_location_lat, business_location_long, first_name, last_name,  role=None, street=None, city=None, state=None, country=None)

@frappe.whitelist(allow_guest=True)
def get_merchant_performance(user_id, seller_id):
    return calculate_merchant_performance(user_id, seller_id)


@frappe.whitelist(allow_guest=True)
def merchant_wallet_balance():
	return get_merchant_balances()