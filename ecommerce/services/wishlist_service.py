import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, CONFLICT
from ecommerce.utils.response_helper import create_response

### Add to wishlist

# def add_to_wishlist(user_id, item_code, is_favourite):
#     try:
#         product_details = frappe.db.get_value(
#             "Products", 
#             {"item_code": item_code}, 
#             ["product_name", "actual_price", "discounted_price", "image", "discount"], 
#             as_dict=True
#         )

#         if not product_details:
#             return create_response(NOT_FOUND, [])

#         existing_wishlist_item = frappe.db.exists(
#             "ProductWishlist", 
#             {"user_id": user_id, "item_code": item_code}
#         )

#         if existing_wishlist_item:
#             return create_response(CONFLICT, {
#                 "message": f"Item {item_code} is already in the wishlist.",
#                 "data": []
#             })

#         # Create a new wishlist entry
#         new_wishlist_item = frappe.get_doc({
#             "doctype": "ProductWishlist",
#             "user_id": user_id,
#             "item_code": item_code,
#             "product_name": product_details["product_name"],
#             "actual_price": product_details["actual_price"],
#             "discounted_price": product_details["discounted_price"],
#             "discount": product_details["discount"],
#             "image": product_details["image"],
#             "is_favourite": is_favourite,
#         })
#         new_wishlist_item.insert(ignore_permissions=True)

#         frappe.db.commit()

#         return create_response(SUCCESS, {
#             "message": f"Item {item_code} added to wishlist successfully!",
#             "data": {
#                 "item_code": item_code,
#                 "product_name": product_details["product_name"],
#                 "actual_price": product_details["actual_price"],
#                 "discounted_price": product_details["discounted_price"],
#                 "discount": product_details["discount"],
#                 "image": product_details["image"]
#             }
#         })

#     except frappe.DuplicateEntryError:
#         return create_response(SERVER_ERROR, {
#             "message": "Duplicate entry found. The item might already be in the wishlist."
#         })
#     except Exception as e:
#         frappe.log_error(
#             f"Error adding item {item_code} to wishlist for user {user_id}: {str(e)}", 
#             "Add to Wishlist Error"
#         )
#         return create_response(SERVER_ERROR, {
#             "message": f"An unexpected error occurred while adding the item: {str(e)}"
#         })


def add_to_wishlist(user_id, products):
    try:
        if not user_id or not products:
            frappe.throw(_("Missing required user ID or products list"))

        # Check for existing wishlist
        existing = frappe.get_all("ProductWishlist", filters={"user_id": user_id}, fields=["name"])
        if existing:
            wishlist_doc = frappe.get_doc("ProductWishlist", existing[0].name)
        else:
            wishlist_doc = frappe.get_doc({
                "doctype": "ProductWishlist",
                "user_id": user_id,
                "products": []
            })

        for product in products:
            wishlist_doc.append("products", {
                "item_code": product.get("item_code"),
                "product_name": product.get("productName"),
                "actual_price": product.get("actual_price"),
                "discounted_price": product.get("discounted_price"),
                "image_url": product.get("images", [{}])[0].get("url", ""),
                "image_alt": product.get("images", [{}])[0].get("alt", ""),
                "image_type": product.get("images", [{}])[0].get("type", "")
            })

        wishlist_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "wishlist_id": wishlist_doc.name,
            "message": "Wishlist updated successfully"
        }

    except Exception as e:
        frappe.log_error(str(e), "Add to Wishlist Error")
        frappe.db.rollback()
        return {"status": "error", "message": f"Failed to add to wishlist: {str(e)}"}




def remove_product_from_wishlist(user_id, product_id):
    try:
        if not user_id or not product_id:
            frappe.throw(_("Missing required user ID or product ID"))

        # Fetch existing wishlist
        wishlist = frappe.get_all("ProductWishlist", filters={"user_id": user_id}, fields=["name"])
        if not wishlist:
            return {
                "status": "error",
                "message": "No wishlist found for this user"
            }

        wishlist_doc = frappe.get_doc("ProductWishlist", wishlist[0].name)

        # Filter out the product to be removed
        updated_products = [
            row for row in wishlist_doc.products if row.item_code != product_id
        ]

        if len(updated_products) == len(wishlist_doc.products):
            return {
                "status": "error",
                "message": "Product not found in wishlist"
            }

        wishlist_doc.set("products", updated_products)
        wishlist_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Product removed from wishlist successfully"
        }

    except Exception as e:
        frappe.log_error(str(e), "Remove from Wishlist Error")
        frappe.db.rollback()
        return {"status": "error", "message": f"Failed to remove product: {str(e)}"}




def get_wishlist(user_id):
    try:
        query = """
            SELECT *
            FROM `tabProductWishlist`
            WHERE user_id = %s
        """
        
        items = frappe.db.sql(query, user_id, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

