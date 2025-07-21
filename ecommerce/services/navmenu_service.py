from frappe import _
import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_nav_menu():
    try:
        menu = {}

        top_level_query = """
            SELECT name 
            FROM `tabItem Group` 
            WHERE is_group = 1 AND parent_item_group = "All Item Groups"
        """
        top_level_items = frappe.db.sql(top_level_query, as_dict=True)

        for top_level in top_level_items:
            submenu = {}

            submenu_query = f"""
                SELECT name 
                FROM `tabItem Group` 
                WHERE is_group = 1 AND parent_item_group = '{top_level.name}'
            """
            submenu_items = frappe.db.sql(submenu_query, as_dict=True)

            for sub_item in submenu_items:
                subsubmenu = set()

                subsubmenu_query = f"""
                    SELECT name 
                    FROM `tabItem Group` 
                    WHERE is_group = 0 AND parent_item_group = '{sub_item.name}'
                """
                subsubmenu_items = frappe.db.sql(subsubmenu_query, as_dict=True)

                for sub_item in subsubmenu_items:
                    subsubmenu.add(sub_item.name)

                submenu[sub_item.name] = subsubmenu

            menu[top_level.name] = submenu

        if not menu:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, menu)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching navigation menu")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


def build_menu_tree(menu_items):
    """Build a tree structure from flat menu data."""
    menu_dict = {item['name']: item for item in menu_items}
    menu_tree = []

    for item in menu_items:
        if not item['parent_menu']:
            menu_tree.append(item)
        else:
            parent = menu_dict.get(item['parent_menu'])
            if parent:
                if 'sub_menu' not in parent:
                    parent['sub_menu'] = []
                parent['sub_menu'].append(item)

    # Sort menus by order
    menu_tree.sort(key=lambda x: x.get('order', 0))
    return menu_tree
