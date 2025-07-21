import frappe

from ecommerce.services.review_service import create_product_review, list_reviews, create_delivery_rating

@frappe.whitelist(allow_guest=True)
def get_review(item_code):
    return list_reviews(item_code)


@frappe.whitelist(allow_guest=True)
def add_review(item_code, user_id, rating, comment):
    return create_product_review(item_code, user_id, rating, comment)


@frappe.whitelist(allow_guest=True)
def add_delivery_rating(item_code, user_id, rating, comment):
    return create_delivery_rating(item_code, user_id, rating, comment)
