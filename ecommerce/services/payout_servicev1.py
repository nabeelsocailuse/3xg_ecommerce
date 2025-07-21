import frappe, json
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

def add_payout_request(args: dict):
	try:
		args = frappe._dict(args)

		cargs = {
			"payout_id": args.id,
			"merchant_id": args.merchant_id,
			"status": args.status,
			"amount": args.amount,
			"doctype": "Payout Request"
		}

		# if(frappe.db.exists('Merchant Wallet Balance', cargs)):
		# 	return create_response(SUCCESS, f"Already have merchant wallet balance.")
		
		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)
		
		return create_response(SUCCESS, {
			"data": doc,
			"message": "Payout request made sucessfully!"
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error creating payout request")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")