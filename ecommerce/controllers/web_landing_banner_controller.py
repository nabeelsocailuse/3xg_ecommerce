import frappe

from ecommerce.services.web_landing_banner_service import get_banner_a, get_banner_b, get_banner_c, get_banner_d, get_banner_e, electronics, computing, phone_tablet, gaming, office

@frappe.whitelist(allow_guest=True)
def list_banner_a():
    return get_banner_a() 

@frappe.whitelist(allow_guest=True)
def list_banner_b():
    return get_banner_b() 

@frappe.whitelist(allow_guest=True)
def list_banner_c():
    return get_banner_c() 


@frappe.whitelist(allow_guest=True)
def list_banner_d():
    return get_banner_d()

@frappe.whitelist(allow_guest=True)
def list_banner_e():
    return get_banner_e() 


@frappe.whitelist(allow_guest=True)
def list_phone_tablet():
    return phone_tablet() 


@frappe.whitelist(allow_guest=True)
def list_electronics():
    return electronics() 


@frappe.whitelist(allow_guest=True)
def list_computing():
    return computing() 


@frappe.whitelist(allow_guest=True)
def list_office():
    return office() 


@frappe.whitelist(allow_guest=True)
def list_gaming():
    return gaming() 
