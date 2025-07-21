import frappe

from ecommerce.services.merchant_review_service import create_merchant_review, list_reviews, get_average_rating


@frappe.whitelist(allow_guest=True)
def add_merchant_review(merchant_id, rating, comment):
    return create_merchant_review(merchant_id, rating, comment)


@frappe.whitelist(allow_guest=True)
def get_merchant_review(merchant_id):
    return list_reviews(merchant_id)



@frappe.whitelist(allow_guest=True)
def get_merchant_average_rating(merchant_id):
    return get_average_rating(merchant_id)
