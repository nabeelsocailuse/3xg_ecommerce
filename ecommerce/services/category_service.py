import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_category():
   
    try:
        query = """
            SELECT name, parent_item_group, is_group
            FROM `tabItem Group`
            WHERE 1=1
        """
        categories = frappe.db.sql(query, as_dict=True)

        if not categories:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, categories)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching categories")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")