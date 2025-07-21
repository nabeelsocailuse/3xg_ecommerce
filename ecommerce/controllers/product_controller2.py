import frappe
from ecommerce.services.product_service import (
    list_items, 
    list_items_category, 
    get_item_by_code, 
    delete_product, 
    get_single_product, 
    list_similar_products, 
    get_all_products_by_merchant_id, 
    get_product_by_merchant_id, 
    reduce_product_quantity, 
    toggle_product_visibility, 
    hide_show, 
    get_product_by_brands, 
    updating_item,
    add_new_item
    )
    
@frappe.whitelist(allow_guest=True)
def get_all_items(product_name=None, min_price=None, max_price=None, color=None, category=None, brand=None, rating=None, discount=None):
    filters = {
        "product_name": product_name,
        "min_price": min_price,
        "max_price": max_price,
        "color": color,
        "category": category,
        "brand": brand,
        "rating": rating,
        "discount": discount
    }
    return list_items(filters)

@frappe.whitelist(allow_guest=True)
def single_product(item_code):
    return get_single_product(item_code)

@frappe.whitelist(allow_guest=True)
def get_all_by_merchant_id(merchant_id):
    return get_all_products_by_merchant_id(merchant_id)

@frappe.whitelist(allow_guest=True)
def get_single_by_merchant(item_code, merchant_id):
    return get_product_by_merchant_id(item_code, merchant_id)

@frappe.whitelist(allow_guest=True)
def get_similar_products(item_code):
    return list_similar_products(item_code)

@frappe.whitelist(allow_guest=True)
def get_all_items_by_category_limit():
    return list_items_category()

@frappe.whitelist(allow_guest=True)
def get_single_item(item_code):
    return get_item_by_code(item_code)

@frappe.whitelist(allow_guest=True)
def get_by_brand(brand):
    return get_product_by_brands(brand)

@frappe.whitelist(allow_guest=True)
def add_item(item_code, **kwargs):
    frappe.log_error(message=f"Incoming kwargs: {kwargs}", title="Debug - Add Item")

    allowed_keys = [
        "product_name", "category", "sub_category", "sub_sub_category",
        "actual_price", "discounted_price", "discount", "image", "images", "rating",
        "brand", "description", "specifications", "collection", "model",
        "weight", "color", "quantity", "warranty", "merchant_id", "status", "createdAt"
    ]

    filtered_kwargs = {key: value for key, value in kwargs.items() if key in allowed_keys}

    return add_new_item(item_code, **filtered_kwargs)

@frappe.whitelist(allow_guest=True)
def update_item(**kwargs):
    return updating_item(kwargs)

@frappe.whitelist(allow_guest=True)
def delete_item(item_code, merchant_id):
    return delete_product(item_code, merchant_id)

@frappe.whitelist(allow_guest=True)
def reduce_quantity(item_code, quantity_to_reduce):
    return reduce_product_quantity(item_code, quantity_to_reduce)

@frappe.whitelist(allow_guest=True)
def toggle_visibility(item_code, merchant_id):
    return toggle_product_visibility(item_code, merchant_id)

@frappe.whitelist(allow_guest=True)
def hide_show_product(item_code, merchant_id):
    return hide_show(item_code, merchant_id)

""" 
Nabeel Saleem
14-01-2025

* Enable product sorting for popularity, time created and price
"""
@frappe.whitelist(allow_guest=True)
def get_sorted_products(popularity=None, time_created=None, price=None):
    from ecommerce.services.product_service import list_sorted_products
    return list_sorted_products(popularity, time_created, price)