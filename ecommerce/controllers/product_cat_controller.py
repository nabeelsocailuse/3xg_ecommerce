import frappe

from ecommerce.services.product_cat_service import get_navbar_menu, create_navbar_data

@frappe.whitelist(allow_guest=True)
def list_navbar():
    return get_navbar_menu() 


@frappe.whitelist(allow_guest=True)
def create_navbar(menu_items):
    return create_navbar_data(menu_items) 