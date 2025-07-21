import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response


def get_navbar_menu():
    try:
        # Fetch top-level menu items
        menu_items = frappe.get_all(
            "Menu Item",
            fields=["name", "title", "url", "order"]
        )

        if not menu_items:
            return create_response(NOT_FOUND, [])

        data = []

        for menu in menu_items:
            frappe.log_error(f"Menu: {menu.name}", "Navbar Menu Debug")

            # Fetch submenu items for the current menu
            submenu_items = frappe.get_all(
                "SubMenu Item",
                filters={"parent_submenu_item": menu.name},
                fields=["name", "title", "url", "order"]
            )
            frappe.log_error(f"Submenus for {menu.name}: {submenu_items}", "Navbar Menu Debug")

            submenu_data = []
            for submenu in submenu_items:
                frappe.log_error(f"Submenu: {submenu.name}", "Navbar Menu Debug")

                subsubmenu_items = frappe.get_all(
                    "SubSubMenu Item",
                    filters={"parent_subsubmenu_item": submenu.name},
                    fields=["title", "url", "order"]
                )
                frappe.log_error(f"SubSubmenus for {submenu.name}: {subsubmenu_items}", "Navbar Menu Debug")

                submenu_data.append({
                    "title": submenu.title,
                    "url": submenu.url,
                    "order": submenu.order,
                    "subsubmenu_items": subsubmenu_items or []
                })

            data.append({
                "title": menu.title,
                "url": menu.url,
                "order": menu.order,
                "submenu_items": submenu_data
            })

        return create_response(SUCCESS, {
            "message": "Navbar menu retrieved successfully.",
            "data": data
        })

    except frappe.DoesNotExistError:
        frappe.log_error("Menu or submenu not found.", "Navbar Menu Retrieval Error")
        return create_response(SUCCESS, {
            "message": "Menu or submenu not found."
        })

    except Exception as e:
        frappe.log_error(f"Unexpected error: {str(e)}", "Navbar Menu Retrieval Error")
        return create_response(SERVER_ERROR, {
            "message": f"An unexpected error occurred: {str(e)}"
        })





def create_navbar_data(menu_items):
    try:
        if not isinstance(menu_items, list) or not all(isinstance(menu, dict) for menu in menu_items):
            raise ValueError("Menu items must be a list of dictionaries.")

        for menu in menu_items:
            if not all(key in menu for key in ["title", "url", "order"]):
                raise ValueError("Each menu item must include 'title', 'url' and 'order'.")

            menu_doc = frappe.get_doc({
                "doctype": "Menu Item",
                "title": menu["title"],
                "url": menu["url"],
                "order": menu["order"]
            })
            menu_doc.insert(ignore_permissions=True)

            if "submenu_items" in menu and isinstance(menu["submenu_items"], list):
                for submenu in menu["submenu_items"]:
                    if not all(key in submenu for key in ["title", "url", "order"]):
                        raise ValueError("Each submenu must include 'title', 'url', and 'order'.")

                    submenu_doc = frappe.get_doc({
                        "doctype": "SubMenu Item",
                        "parent_menu_item": menu_doc.name,
                        "title": submenu["title"],
                        "url": submenu["url"],
                        "order": submenu["order"]
                    })
                    submenu_doc.insert(ignore_permissions=True)

                    if "subsubmenu_items" in submenu and isinstance(submenu["subsubmenu_items"], list):
                        for subsubmenu in submenu["subsubmenu_items"]:
                            if not all(key in subsubmenu for key in ["title", "url", "order"]):
                                raise ValueError("Each sub-submenu must include 'title', 'url', and 'order'.")

                            subsubmenu_doc = frappe.get_doc({
                                "doctype": "SubSubMenu Item",
                                "parent_menu_item": submenu_doc.name,
                                "title": subsubmenu["title"],
                                "url": subsubmenu["url"],
                                "order": subsubmenu["order"]
                            })
                            subsubmenu_doc.insert(ignore_permissions=True)

        frappe.db.commit()
        return create_response(SUCCESS, {"message": "Navbar data created successfully."})

    except ValueError as e:
        frappe.log_error(f"Validation error while creating navbar: {str(e)}", "Navbar Data Creation Validation Error")
        return create_response(BAD_REQUEST, {"message": f"Validation error: {str(e)}"})

    except frappe.ValidationError as e:
        frappe.log_error(f"Frappe validation error: {str(e)}", "Navbar Data Creation Validation Error")
        return create_response(BAD_REQUEST, {"message": f"Frappe validation error: {str(e)}"})

    except Exception as e:
        frappe.log_error(f"Unexpected error while creating navbar data: {str(e)}", "Navbar Data Creation Error")
        return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})
