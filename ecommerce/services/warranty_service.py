import frappe
from frappe import _
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response
from datetime import datetime



def list_by_imei(imei):
    try:
        query = """
            SELECT *
            FROM `tabWarranty`
            WHERE imei = %s
        """
        
        warranty_details = frappe.db.sql(query, (imei,), as_dict=True)

        if not warranty_details:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, {
            "message": "Warranty details retrieved successfully.",
            "data": warranty_details
        })

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, {
            "message": "Warranty details not found.",
            "error": str(e)
        })
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching Warranty details")
        return create_response(SERVER_ERROR, {
            "message": "An unexpected error occurred.",
            "error": str(e)
        })



def check_imei_exist(imei):
    try:
        imei_query = """
            SELECT *
            FROM `tabWarranty`
            WHERE imei = %s
        """
        imei_exists = frappe.db.sql(imei_query, (imei,), as_dict=True)

        if not imei_exists:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, {
            "message": "IMEI exists in the database.",
            "data": imei_exists
        })

    except frappe.DoesNotExistError:
        return create_response(SUCCESS, {
            "message": "Warranty record not found. Please check the provided IMEI.",
            "data": []
        })

    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error while checking IMEI: {str(e)}", "Check IMEI Error")
        return create_response(SERVER_ERROR, {
            "message": f"Validation Error: {str(e)}"
        })

    except Exception as e:
        frappe.log_error(f"Unexpected error while checking IMEI: {str(e)}", "Check IMEI Error")
        return create_response(SERVER_ERROR, {
            "message": f"An unexpected error occurred: {str(e)}"
        })




def mark_warranty_as_claimed(user_id, imei, brand_model, address, area, date, time, complain):
    try:
        warranty_doc = frappe.get_doc("Warranty", {"imei": imei})
        
        if not warranty_doc:
            return create_response(NOT_FOUND, [])
        
        user_details = frappe.db.get_value(
                "Website User",
                {"user_id": user_id},
                "*",
                as_dict=True
            )
        
        warranty_doc.claimed_by = user_id
        warranty_doc.is_claimed = 1
        warranty_doc.save(ignore_permissions=True)
        
        warranty_claim_doc = frappe.get_doc({
            "doctype": "Warranty",
            "user_id": user_id,
            "imei": imei,
            "brand_model": brand_model,
            "address": address,
            "area": area,
            "pickup_date": date,
            "pickup_time": time,
            "complain": complain,
        })
        
        warranty_claim_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return create_response(SUCCESS, {
            "message": f"Warranty {imei} marked as claimed by {user_id} successfully!",
            "data": {
                "warranty_id": warranty_doc.name,
                "imei": warranty_doc.imei,
                "claimed_by": user_details["first_name"],
                "is_claimed": warranty_doc.is_claimed
            }
        })

    except frappe.DoesNotExistError:
        return create_response(SUCCESS, "Warranty not found. Please check the provided IMEI.")
    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error while marking warranty as claimed: {str(e)}", "Mark Warranty as Claimed Error")
        return create_response(BAD_REQUEST, f"Validation Error: {str(e)}")
    except Exception as e:
        frappe.log_error(f"Error marking warranty as claimed: {str(e)}", "Mark Warranty as Claimed Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

    


def get_claimed_warranties(user_id):
    try:
        query = """
            SELECT *
            FROM `tabWarranty`
            WHERE is_claimed = 1 AND user_id = %s
        """
        warranties = frappe.db.sql(query, user_id, as_dict=True)

        if not warranties:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, {
            "message": "Claimed warranties retrieved successfully.",
            "data": warranties
        })

    except frappe.DoesNotExistError:
        return create_response(SUCCESS, {
            "message": "No claimed warranties found for the provided user ID."
        })

    except frappe.ValidationError as e:
        frappe.log_error(
            f"Validation error while retrieving claimed warranties: {str(e)}",
            "Get Claimed Warranties Error"
        )
        return create_response(SERVER_ERROR, {
            "message": f"Validation Error: {str(e)}"
        })

    except Exception as e:
        frappe.log_error(
            f"Unexpected error while retrieving claimed warranties: {str(e)}",
            "Get Claimed Warranties Error"
        )
        return create_response(SERVER_ERROR, {
            "message": f"An unexpected error occurred: {str(e)}"
        })




def get_warranties_by_imei(user_id, imei):
    try:
        query = """
            SELECT *
            FROM `tabWarranty`
            WHERE user_id = %s AND imei = %s
        """

        warranties = frappe.db.sql(query, (user_id, imei), as_dict=True)

        if not warranties:
            return create_response(NOT_FOUND, {})

        return create_response(SUCCESS, warranties[0])

    except frappe.DoesNotExistError:
        return create_response(SUCCESS, _("IMEI not found. Please check the provided IMEI."))

    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error while getting warranties by IMEI: {str(e)}", "Get Warranties by IMEI Error")
        return create_response(SERVER_ERROR, f"Validation Error: {str(e)}")
    
    except Exception as e:
        frappe.log_error(f"Unexpected error while getting warranties by IMEI: {str(e)}", "Get Warranties by IMEI Error")
        return create_response(SERVER_ERROR, _("Unexpected Error: ") + str(e))

    

def get_active_warranty(user_id):
    try:

        select_query = """
            SELECT *
            FROM `tabWarranty`
            WHERE is_active = 1 AND user_id = %s
        """
        warranties = frappe.db.sql(select_query, (user_id,), as_dict=True)

        if not warranties:
            return create_response(SUCCESS, [])

        return create_response(SUCCESS, warranties)
    
    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error while getting active warranties: {str(e)}", "Get Active Warranties Error")
        return create_response(SERVER_ERROR, f"Validation Error: {str(e)}")
    
    except Exception as e:
        frappe.log_error(f"Unexpected error: {str(e)}", "Get Active Warranties Error")
        return create_response(SERVER_ERROR, f"Unexpected Error: {str(e)}")

    


def get_expired_warranty(user_id):
    try:
        current_date = datetime.now()

        update_query = """
            UPDATE `tabWarranty`
            SET is_active = 0
            WHERE warranty_expiry_date < %s AND is_active = 1 AND user_id = %s
        """
        frappe.db.sql(update_query, (current_date, user_id))

        select_query = """
            SELECT *
            FROM `tabWarranty`
            WHERE is_active = 0 AND user_id = %s
        """
        warranties = frappe.db.sql(select_query, (user_id,), as_dict=True)

        if not warranties:
            return create_response(SUCCESS, {
                "message": "No expired warranties found for the given user.",
                "data": []
            })

        return create_response(SUCCESS, {
            "message": "Expired warranties retrieved successfully.",
            "data": warranties
        })
    
    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error while getting expired warranties: {str(e)}", "Get Expired Warranties Error")
        return create_response(SERVER_ERROR, f"Validation Error: {str(e)}")
    
    except Exception as e:
        frappe.log_error(f"Unexpected error while getting expired warranties: {str(e)}", "Get Expired Warranties Error")
        return create_response(SERVER_ERROR, f"Unexpected Error: {str(e)}")

    


def apply_for_warranty(user_id, imei, brand_model, address, area, date, time, complain):
    try:
          
        warranty_details = frappe.get_doc({
            "doctype": "Warranty",
            "user_id": user_id,
            "imei": imei,
            "brand_model": brand_model,
            "address": address,
            "area": area,
            "pickup_date": date,
            "pickup_time": time,
            "complain": complain,
        })
        
        warranty_details.insert(ignore_permissions=True)
        frappe.db.commit()

        return create_response(SUCCESS, {
            "message": "Warranty created successfully!",
            "data": warranty_details
        })

    except ValueError as e:
        frappe.log_error(f"Data validation error for warranty: {str(e)}", "Warranty Creation Validation Error")
        return create_response(BAD_REQUEST, f"Validation error: {str(e)}")

    except frappe.ValidationError as e:
        frappe.log_error(f"Frappe validation error for warranty: {str(e)}", "Warranty Creation Validation Error")
        return create_response(BAD_REQUEST, f"Frappe validation error: {str(e)}")

    except Exception as e:
        frappe.log_error(f"Error creating warranty for warranty: {str(e)}", "Warranty Creation Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
        
        
        
        
def create_warranty_logic(order_item_id, imei, warranty_expiry_date, user_id):
    try:
        warranty_doc = frappe.get_doc({
            "doctype": "Warranty",
            "order_item_id": order_item_id, 
            "imei": imei, 
            "warranty_expiry_date": warranty_expiry_date, 
            "user_id": user_id,
            
        })

        warranty_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return create_response(SUCCESS, {
            "message": "Warranty record created successfully!",
            "data": {
                "name": warranty_doc.name,
                "user_id": warranty_doc.user_id,
                "imei": warranty_doc.imei,
                "order_item_id": warranty_doc.order_item_id,
                "warranty_expiry_date": warranty_doc.warranty_expiry_date
                
            }
        })

    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error creating Warranty: {str(e)}", "Warranty Creation Error")
        return create_response(BAD_REQUEST, f"Validation error: {str(e)}")

    except Exception as e:
        frappe.log_error(f"Unexpected error creating Warranty: {str(e)}", "Warranty Creation Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def create_warranty_claim_logic(warranty_id, imei, brand_model, service_address, area, pickup_date, pickup_time, device_issue):
    try:
        doc = frappe.get_doc({
            "doctype": "Warranty Claim",
            "warranty_id": warranty_id,
            "serial_no": imei,
            "brand_model": brand_model,
            "address": service_address,
            "area": area,
            "pickup_date": pickup_date,
            "pickup_time": pickup_time,
            "issue": device_issue,
            "status": "Open"
        })

        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return create_response(SUCCESS, {
            "message": "Warranty claim created successfully.",
            "data": {
                "name": doc.name,
                "serial_no": doc.serial_no,
                "status": doc.status,
                "pickup_date": doc.pickup_date,
                "issue": doc.issue
            }
        })

    except frappe.ValidationError as e:
        frappe.log_error(str(e), "Warranty Claim Validation Error")
        return create_response(BAD_REQUEST, f"Validation error: {str(e)}")

    except Exception as e:
        frappe.log_error(str(e), "Warranty Claim Creation Error")
        return create_response(SERVER_ERROR, f"Unexpected error: {str(e)}")
