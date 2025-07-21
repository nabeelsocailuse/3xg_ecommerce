import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_banner_a():
   
    try:
        query = """
            SELECT *
            FROM `tabWeb LandingBannerA`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    
    
def get_banner_b():
   
    try:
        query = """
            SELECT *
            FROM `tabWeb LandingBannerB`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    
    
def get_banner_c():
   
    try:
        query = """
            SELECT *
            FROM `tabWeb LandingBannerC`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    
    
def get_banner_d():
   
    try:
        query = """
            SELECT *
            FROM `tabWeb LandingBannerD`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            raise create_response(NOT_FOUND, {
                "message": "No items found.",
                "data": []
            })

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    
    
def get_banner_e():
   
    try:
        query = """
            SELECT *
            FROM `tabWeb LandingBannerE`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    


def electronics():
   
    try:
        query = """
            SELECT *
            FROM `tabElectronics Banner`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    


def office():
   
    try:
        query = """
            SELECT *
            FROM `tabOfficeEquip Banner`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def phone_tablet():
   
    try:
        query = """
            SELECT *
            FROM `tabPhoneTablet Banner`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    

def gaming():
   
    try:
        query = """
            SELECT *
            FROM `tabGaming Banner`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


def computing():
   
    try:
        query = """
            SELECT *
            FROM `tabComputing Banner`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")