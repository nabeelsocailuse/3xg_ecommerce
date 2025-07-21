import frappe
from ecommerce.services.wishlist_service import remove_product_from_wishlist, get_wishlist, add_to_wishlist
    

# @frappe.whitelist(allow_guest=True)
# def add_wishlist(user_id, item_code, is_favourite=False):
#     return add_to_wishlist(user_id, item_code, is_favourite)

@frappe.whitelist(allow_guest=True)
def add_wishlist():
    data = frappe.request.get_json()
    user_id = data.get("user_id")
    products = data.get("products", [])
    return add_to_wishlist(user_id, products)



@frappe.whitelist(allow_guest=True)
def remove_wishlist():
    data = frappe.request.get_json()
    user_id = data.get("user_id")
    item_code = data.get("item_code")

    if not user_id or not item_code:
        return {
            "status": "error",
            "message": "Missing user_id or item_code"
        }

    return remove_product_from_wishlist(user_id, item_code)


@frappe.whitelist(allow_guest=True)
def get_wishlist_item(user_id):
    return get_wishlist(user_id)