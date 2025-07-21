import frappe
""" 
{
    'status': 'arriving_pickup', 
    'order_id': '9df96519-21f9-4928-b1a4-f1e61114261f', 
    'pickupCode': '196007', 
    'trackingCode': None, 
    'cmd': 'ecommerce.controllers.itranxit_controller.receive_itranxit_order_status'
}
"""
@frappe.whitelist(allow_guest=True)
def receive_itranxit_order_status(**kwargs):
    args = frappe._dict(kwargs)
    doc  = frappe.get_doc("iTranxit Order Shipment", {"order_id": args.order_id})
    doc.status = args.status
    doc.pickup_code = args.pickupCode
    doc.tracking_code = args.trackingCode
    doc.save(ignore_permissions=True)
    frappe.db.commit()

# https://zirconprod.3xg.africa/api/method/ecommerce.controllers.itranxit_controller.receive_itranxit_order_status

# bench --site zirconprod.3xg.africa execute ecommerce.controllers.itranxit_controller.get_decrypted_password
# def get_decrypted_password():
#     from frappe.utils.password import get_decrypted_password
#     pwd = get_decrypted_password("Email Account", "Supports", fieldname="password", raise_exception=True)
#     print(pwd)