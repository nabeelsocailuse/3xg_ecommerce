import frappe

from ecommerce.services.shipment_service import create_shipment, update_shipment_status, track_shipment, delete_shipment


@frappe.whitelist(allow_guest=True)
def create_order_shipment(order_id, user_id, shipping_address, first_name, last_name, phone_number, lga, postal_code, latitude, longitude):
    return create_shipment(order_id, user_id, shipping_address, first_name, last_name, phone_number, lga, postal_code, latitude, longitude)

@frappe.whitelist(allow_guest=True)
def update_status(order_id, new_status):
    return update_shipment_status(order_id, new_status)

@frappe.whitelist(allow_guest=True)
def track_shipments(user_id, order_id):
    return track_shipment(user_id, order_id)


@frappe.whitelist(allow_guest=True)
def remove_shipment(user_id, order_id):
    return delete_shipment(user_id, order_id)