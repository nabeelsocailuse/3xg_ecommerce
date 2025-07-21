import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

def create_shipment(order_id, user_id, shipping_address, first_name, last_name, phone_number, lga, postal_code, latitude, longitude):
    try:
        frappe.logger().info(f"Received request to create shipment for order_id: {order_id}, user_id: {user_id}")

        order = frappe.db.get_value(
            "Order", 
            {"order_id": order_id, "user_id": user_id}, 
            "*", 
            as_dict=True
        )
        if not order:
            return create_response(NOT_FOUND, [])

        existing_shipment = frappe.db.get_value("Order Shipment", {"order_id": order_id}, "name")
        frappe.logger().debug(f"Existing shipment fetched: {existing_shipment}")

        if existing_shipment:
            return create_response(SERVER_ERROR, {
                "message": "A shipment already exists for this order.",
                "data": {"order_id": existing_shipment}
            })

        shipment_doc = frappe.get_doc({
            "doctype": "Order Shipment",
            "order_id": order_id,
            "user_id": user_id,
            "status": "Shipment Created",
            "shipping_address": shipping_address,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "lga": lga,
            "postal_code": postal_code,
            "latitude": latitude,
            "longitude": longitude,
        })
        shipment_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return create_response(SUCCESS, {
            "message": f"Shipment {order_id} created successfully!",
            "data": {"order_id": shipment_doc.name}
        })

    except frappe.DuplicateEntryError:
        return create_response(SERVER_ERROR, "A shipment already exists for this order.")
    except frappe.DoesNotExistError:
        return create_response(SUCCESS, "Order not found. Please check the provided details.")
    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error while creating shipment: {str(e)}", "Create Shipment Error")
        return create_response(SERVER_ERROR, f"Validation Error: {str(e)}")
    except Exception as e:
        frappe.log_error(f"Unexpected error while creating shipment: {str(e)}", "Create Shipment Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def update_shipment_status(order_id, new_status):
    try:
        shipment = """
            SELECT *
            FROM `tabOrder Shipment`
            WHERE order_id = %s
        """
        order_id = frappe.db.sql(shipment, (order_id), as_dict=True)
        
        if not shipment:
            return create_response(NOT_FOUND, [])
        
        shipment_doc = frappe.get_doc("Order Shipment", order_id)
        shipment_doc.status = new_status
        
        shipment_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return create_response(SUCCESS, {
            "message": f"Shipment status updated successfully!",
            "data": {"shipment_id": shipment_doc.order_id, "status": shipment_doc.status}
        })

    except frappe.DoesNotExistError:
        return create_response(SUCCESS, "Shipment not found. Please check the provided Shipment ID.")
    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error while updating shipment status: {str(e)}", "Update Shipment Status Error")
        return create_response(SERVER_ERROR, f"Validation Error: {str(e)}")
    except Exception as e:
        frappe.log_error(f"Unexpected error while updating shipment status: {str(e)}", "Update Shipment Status Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def track_shipment(user_id, order_id):
    try:
        shipment_query = """
            SELECT *
            FROM `tabOrder Shipment`
            WHERE user_id = %s AND order_id = %s
        """
        shipment = frappe.db.sql(shipment_query, (user_id, order_id), as_dict=True)

        if not shipment:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, {"message": "Shipment retrieved successfully.", "data": shipment})

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, {"message": f"Shipment not found: {str(e)}"})
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching shipment")
        return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})
    
    
    
def delete_shipment(order_id, user_id):
    try:
        frappe.logger().info(f"Received request to delete shipment for order_id: {order_id}, user_id: {user_id}")

        # Check if shipment exists
        shipment_name = frappe.db.get_value(
            "Order Shipment", 
            {"order_id": order_id, "user_id": user_id}, 
            "name"
        )
        frappe.logger().debug(f"Fetched shipment name for deletion: {shipment_name}")

        if not shipment_name:
            return create_response(NOT_FOUND, [])

        # Delete the shipment
        frappe.delete_doc("Order Shipment", shipment_name, ignore_permissions=True)
        frappe.db.commit()

        return create_response(SUCCESS, {
            "message": f"Shipment for order_id {order_id} deleted successfully!",
            "data": {"order_id": order_id}
        })

    except frappe.DoesNotExistError:
        return create_response(SUCCESS, {
            "message": "Shipment not found. Please check the provided details.",
            "data": []
        })
    except Exception as e:
        frappe.log_error(f"Unexpected error while deleting shipment: {str(e)}", "Delete Shipment Error")
        return create_response(SERVER_ERROR, {
            "message": f"An unexpected error occurred: {str(e)}",
            "data": []
        })
