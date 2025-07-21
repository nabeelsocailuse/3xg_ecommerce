import frappe, json
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response


def add_payout_request(args: dict):
	try:
		args = frappe._dict(args)

		# Check if merchant exists
		merchant_exists = frappe.db.exists("Merchants", {"merchant_id": args.merchant_id})
		
		if not merchant_exists:
			return create_response(NOT_FOUND, "Merchant not registered. Please complete registration before making a payout request.")

		# Convert amount from Kobo to Naira
		amount_in_naira = float(args.amount) / 100

		cargs = {
			"payout_id": args.id,
			"merchant_id": args.merchant_id,
			"status": args.status,
			"amount": amount_in_naira,
			"merchant_email": args.merchant_email,
			"merchant_fullname": args.merchant_fullname,
			"doctype": "Payout Request"
		}

		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)

		return create_response(SUCCESS, {
			"data": doc,
			"message": "Payout request made successfully!"
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error creating payout request")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
