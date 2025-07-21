import frappe

from ecommerce.services.kyc_service import get_kycs, get_kyc_by_id, add_new_kyc

@frappe.whitelist(allow_guest=True)
def list_kyc():
    return get_kycs() 


@frappe.whitelist(allow_guest=True)
def get_kyc_by_merchant(merchant_id):
    return get_kyc_by_id(merchant_id)

@frappe.whitelist(allow_guest=True)
def add_kyc(merchant_id, kyc_id, kyc_type, image=None, status=None, **kwargs):
    
    return add_new_kyc(merchant_id, kyc_id, kyc_type, image, status)

