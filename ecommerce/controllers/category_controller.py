import frappe

from ecommerce.services.category_service import get_category

@frappe.whitelist(allow_guest=True)
def list_category():
    return get_category() 