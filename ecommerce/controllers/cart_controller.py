import frappe

from ecommerce.services.cart_service import ( 
    create_update_cart, 
    read_cart_list,
    update_cart_quantity, 
    delete_cart
)

@frappe.whitelist(allow_guest=True)
def create_update(**kwargs):
    return create_update_cart(kwargs)

@frappe.whitelist(allow_guest=True)
def read(userId):
    return read_cart_list(userId)

'''@frappe.whitelist(allow_guest=True)
def update_cart_item(user_id, item_code, quantity):
    return update_cart_quantity(user_id, item_code, quantity)

@frappe.whitelist(allow_guest=True)
def delete_cart_item(user_id, item_code):
    return delete_cart(user_id, item_code)'''

@frappe.whitelist(allow_guest=True)
def delete(userId):
    return delete_cart(userId)
