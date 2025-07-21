import frappe

from ecommerce.services.navmenu_service import get_nav_menu, build_menu_tree

@frappe.whitelist(allow_guest=True)
def list_navmenu():
    return get_nav_menu() 


@frappe.whitelist(allow_guest=True)
def create_navmenu():
    return build_menu_tree() 