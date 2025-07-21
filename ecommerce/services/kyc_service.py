import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_kycs():
   
    try:
        query = """
            SELECT *
            FROM `tabKYC`
            WHERE 1=1
        """
         
        merchants = frappe.db.sql(query, as_dict=True)

        if not merchants:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, merchants)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching KYC")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def get_kyc_by_id(merchant_id):
    try:
        query = """
            SELECT *
            FROM `tabKYC`
            WHERE merchant_id = %s
        """
        
        kyc_record = frappe.db.sql(query, (merchant_id), as_dict=True)

        if not kyc_record:
            return create_response(NOT_FOUND, {
                "message": "KYC record not found.",
                "data": []
            })

        return create_response(SUCCESS, {
            "message": "KYC fetched successfully.",
            "data": kyc_record[0]
        })

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, {
            "message": "KYC record does not exist.",
            "error": str(e)
        })
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching KYC by ID")
        return create_response(SERVER_ERROR, {
            "message": "An unexpected error occurred while fetching KYC.",
            "error": str(e)
        })




### Add new item
def add_new_kyc(merchant_id, kyc_id, kyc_type, image, status):
    
    try:
        if frappe.db.exists("KYC", {"kyc_id": kyc_id}):
            raise ValueError(f"Merchant with code '{kyc_id}' already exists!")
 
                
        new_item = frappe.get_doc({
            "doctype": "KYC",
            "merchant_id": merchant_id,
            "kyc_id": kyc_id,
            "type": kyc_type,
            "image": image,
            "status": status,
        })
        new_item.insert(ignore_permissions=True)
        frappe.db.commit()

        return create_response(SUCCESS, f"KYC '{kyc_id}' added successfully!")

    except ValueError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(f"Error adding new KYC '{merchant_id}': {str(e)}", "Add KYC Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
