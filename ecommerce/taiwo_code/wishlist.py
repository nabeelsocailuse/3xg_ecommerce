import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

@frappe.whitelist(allow_guest=True)
def add_wishlist(user_id, item_code, is_favourite):
    return add_to_wishlist(user_id, item_code, is_favourite)


def add_to_wishlist(user_id, item_code, is_favourite):
    try:
        product_details = frappe.db.get_value(
            "Products", 
            {"item_code": item_code}, 
            ["product_name", "discounted_price", "image"], 
            as_dict=True
        )

        if not product_details:
            return create_response(SUCCESS, {
                "message": "No product found.",
                "data": []
            })

        new_wishlist_item = frappe.get_doc({
            "doctype": "ProductWishlist",
            "user_id": user_id,
            "item_code": item_code,
            "product_name": product_details["product_name"],
            "price": product_details["discounted_price"],
            "image": product_details["image"],
            "is_favourite": is_favourite,
        })
        new_wishlist_item.insert()

        frappe.db.set_value("Products", {"item_code": item_code}, "is_favourite", 1)

        frappe.db.commit()

        return create_response(SUCCESS, f"Item {item_code} added to wishlist successfully and marked as favourite!")

    except frappe.DuplicateEntryError:
        return create_response(SERVER_ERROR, "Duplicate entry found. Please try again.")
    except Exception as e:
        frappe.log_error(f"Error adding item {item_code} to wishlist for user {user_id}: {str(e)}", "Add to wishlist Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred while adding the item: {str(e)}")

