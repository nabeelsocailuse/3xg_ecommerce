import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_category_list():
   
    try:
        query = """
            SELECT *
            FROM `tabCategory`
            WHERE 1=1
        """
         
        brands = frappe.db.sql(query, as_dict=True)

        if not brands:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, brands)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching category")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    

def get_subcategory_list():
   
    try:
        query = """
            SELECT *
            FROM `tabSubCategory`
            WHERE 1=1
        """
         
        brands = frappe.db.sql(query, as_dict=True)

        if not brands:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, brands)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching subcategory")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    

def get_sub_sub_category_list():
   
    try:
        query = """
            SELECT *
            FROM `tabSubSubCategory`
            WHERE 1=1
        """
         
        brands = frappe.db.sql(query, as_dict=True)

        if not brands:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, brands)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching sub subcategory")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    
    

