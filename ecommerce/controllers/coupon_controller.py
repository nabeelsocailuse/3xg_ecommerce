import frappe

from ecommerce.services.coupon_service import (
	get_coupons_list
)

@frappe.whitelist(allow_guest=True)
def get_coupons(**kwargs):
	return get_coupons_list(kwargs)