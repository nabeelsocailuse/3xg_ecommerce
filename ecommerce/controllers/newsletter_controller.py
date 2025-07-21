import frappe
from ecommerce.services.newsletter_service import (
    subscribe_unsubscribe_newsletter
)

@frappe.whitelist(allow_guest=True)
def sub_unsub_newsletter(**kwargs):
    return subscribe_unsubscribe_newsletter(kwargs)