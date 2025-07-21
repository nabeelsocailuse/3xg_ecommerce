import frappe

from ecommerce.services.banners_service import (
	get_promotional_banners,
	get_home_banners
)

@frappe.whitelist(allow_guest=True)
def read(**kwargs):
	return get_promotional_banners(kwargs)

# https://zirconstage.3xg.africa/api/method/ecommerce.controllers.banners_controller.home_banners
@frappe.whitelist(allow_guest=True)
def home_banners(**kwargs):
	return get_home_banners(kwargs)
