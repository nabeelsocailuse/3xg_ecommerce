import frappe

from ecommerce.services.warranty_service import check_imei_exist, mark_warranty_as_claimed, get_claimed_warranties, get_warranties_by_imei, get_active_warranty, get_expired_warranty, list_by_imei, apply_for_warranty, create_warranty_logic, create_warranty_claim_logic

# Constants for HTTP-like status codes
SUCCESS = 200
BAD_REQUEST = 400
SERVER_ERROR = 500

# Helper function to standardize responses
def create_response(status, data):
    return {
        "status": status,
        "data": data
    }


@frappe.whitelist(allow_guest=True)
def get_imei():
    return list_by_imei()


@frappe.whitelist(allow_guest=True)
def check_warranty(imei):
    return check_imei_exist(imei)


@frappe.whitelist(allow_guest=True)
def mark_as_claimed(user_id, imei, brand_model, address, area, date, time, complain):
    return mark_warranty_as_claimed(user_id, imei, brand_model, address, area, date, time, complain)


@frappe.whitelist(allow_guest=True)
def get_claimed(user_id):
    return get_claimed_warranties(user_id)


@frappe.whitelist(allow_guest=True)
def get_by_imei(user_id, imei):
    return get_warranties_by_imei(user_id, imei)


@frappe.whitelist(allow_guest=True)
def get_active(user_id):
    return get_active_warranty(user_id)


@frappe.whitelist(allow_guest=True)
def get_expired(user_id):
    return get_expired_warranty(user_id)


@frappe.whitelist(allow_guest=True)
def apply_warranty(user_id, imei, brand_model, address, area, date, time, complain):
    return apply_for_warranty(user_id, imei, brand_model, address, area, date, time, complain) 


# @frappe.whitelist(allow_guest=True)
# def create_warranty(order_item_id, imei, warranty_expiry_date, user_id):
#     return create_warranty_logic(order_item_id, imei, warranty_expiry_date, user_id)

@frappe.whitelist(allow_guest=True)
def create_warranty():
    import json

    data = frappe.local.form_dict

    # If empty, parse raw JSON
    if not data.get("order_item_id"):
        try:
            data = json.loads(frappe.request.data)
        except Exception as e:
            return create_response(BAD_REQUEST, f"Invalid JSON: {str(e)}")

    return create_warranty_logic(
        data.get("order_item_id"),
        data.get("imei"),
        data.get("warranty_expiry_date"),
        data.get("user_id")
    )


@frappe.whitelist(allow_guest=True)
def create_warranty_claim():
    import json

    try:
        data = frappe.local.form_dict

        if not data.get("warrantyId"):
            data = json.loads(frappe.request.data)

        warranty_id = data.get("warrantyId")
        imei = data.get("imei")
        brand_model = data.get("brand_model")
        service_address = data.get("address")
        area = data.get("area")
        pickup_date = data.get("pickupDate")
        pickup_time = data.get("pickupTime")
        device_issue = data.get("deviceIssue")

        if not all([warranty_id, imei, brand_model, service_address, area, pickup_date, pickup_time, device_issue]):
            return create_response(BAD_REQUEST, error="Missing one or more required fields")

        return create_warranty_claim_logic(
            warranty_id, imei, brand_model, service_address,
            area, pickup_date, pickup_time, device_issue
        )

    except Exception as e:
        frappe.log_error(str(e), "Warranty Claim Creation Error")
        return create_response(SERVER_ERROR, f"An error occurred: {str(e)}")
