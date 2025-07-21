import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now
import json

@frappe.whitelist(allow_guest=True)
def create_transaction():
    try:
        data = json.loads(frappe.request.data)

        
        doc = frappe.get_doc({
            "doctype": "Transaction",  
            "amount": data["amount"],
            "reference": data["reference"],
            "status": data["status"],
            "type": data["type"],
            "description": data.get("description", ""),
            "external_reference": data.get("externalReference", ""),
            "payment_provider": data.get("paymentProvider", ""),
            "release_date": data.get("releaseDate", None),
            "created_at": data.get("createdAt", now()),
            "user_id": data["userId"],
            "fees": data.get("fees", 0),
        })

        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Transaction created successfully",
            "transaction_id": doc.name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Transaction Error")
        frappe.response['http_status_code'] = 400
        return {
            "status": "error",
            "message": str(e)
        }
