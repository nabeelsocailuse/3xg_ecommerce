import frappe

from ecommerce.services.merchant_category_service import get_category_list, get_subcategory_list, get_sub_sub_category_list

@frappe.whitelist(allow_guest=True)
def list_categories():
    return get_category_list()


@frappe.whitelist(allow_guest=True)
def list_sub_categories():
    return get_subcategory_list()


@frappe.whitelist(allow_guest=True)
def list_sub_sub_categories():
    return get_sub_sub_category_list()

