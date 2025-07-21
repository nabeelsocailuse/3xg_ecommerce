import frappe

from ecommerce.services.brand_service import get_brands, get_best_selling_brands, get_single_brand

@frappe.whitelist(allow_guest=True)
def list_brand():
    return get_brands()


@frappe.whitelist(allow_guest=True)
def list_single_brand(name):
    return get_single_brand(name)

# Nabeel Saleem, 23-12-2024
@frappe.whitelist(allow_guest=True)
def list_of_best_selling_brands(category=None, brand=None, model=None, date=None):
    return get_best_selling_brands(category, brand, model, date)