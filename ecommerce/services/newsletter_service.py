import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

def subscribe_unsubscribe_newsletter(args: dict):
	try:
		args = frappe._dict(args)
		doctype = "Email Group Member"
		cargs = {
			"email_group": "3xg News Letter", 
			"email": args.email
		}
		if(frappe.db.exists(doctype, cargs)):
			name = frappe.get_value(doctype, cargs, "name")
			doc = frappe.get_doc(doctype, name)
			doc.unsubscribed = 0 if(args.status) else 1
			doc.save(ignore_permissions=True)
			return doc
		else:
			cargs.update({
				"doctype": doctype,
				"unsubscribed": 0 if(args.status) else 1,
				"source": "Newsletter",
			})
			doc = frappe.get_doc(cargs)
			doc.insert(ignore_permissions=True)

		return create_response(SUCCESS, {"data": doc})

	except ValueError as e:
		frappe.log_error(f"Data validation error", "Newsletter subscription error")
		return create_response(BAD_REQUEST, {"message": f"Validation error: {str(e)}"})
	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error: {str(e)}", "Newsletter subscription error")
		return create_response(BAD_REQUEST, {"message": f"Frappe validation error: {str(e)}"})
	except Exception as e:
		frappe.log_error(f"Error creating Newsletter: {str(e)}", "Newsletter subscription error")
		return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})



