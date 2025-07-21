import frappe, json
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

def adding(args: dict):
	try:
		args = frappe._dict(args)

		# create email group member
		cargs = {
			"user_type": args.user_type,
			"user_id": args.user_id,
			"email": args.email,
			"amount": args.amount,
			"merchant_id": args.user_id if(args.user_type=="merchant") else "",
			"website_user": args.user_id if(args.user_type=="customer") else "",
		}

		# verify email
		if(frappe.db.exists('Wallet', cargs)):
			return create_response(SUCCESS, f"Already have wallet balance.")

		cargs.update({"doctype": "Wallet"})
		
		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)
		
		return create_response(SUCCESS, {
			"data": doc,
			"message": "Wallet balance added sucessfully!"
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error creating wallet balance")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def updating(args: dict):
	try:
		args = frappe._dict(args)

		# create email group member
		cargs = {
			"user_type": args.user_type,
			"user_id": args.user_id,
			"email": args.email,
			# "amount": args.amount,
			# "merchant_id": args.user_id if(args.user_type=="merchant") else "",
			# "website_user": args.user_id if(args.user_type=="customer") else "",
		}
			
		# verify email
		if(frappe.db.exists('Wallet', cargs)):
			wallet_id = frappe.db.get_value("Wallet", cargs, "name")
			if(wallet_id): 
				doc = frappe.get_doc("Wallet", wallet_id)
				doc.amount =  args.amount
				doc.save(ignore_permissions=True)
				return create_response(SUCCESS, f"Wallet balance updated success.{doc}")

		
		
		return create_response(NOT_FOUND, {
			"data": args,
			"message": "Wallet balance not found. Add it first."
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error updating wallet balance")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def getting(args: dict):
	try:
		args = frappe._dict(args)

		# create email group member
		filters = frappe._dict({
			"user_type": args.user_type,
			"user_id": args.user_id,
			# "amount": args.amount,
			# "merchant_id": args.user_id if(args.user_type=="merchant") else "",
			# "website_user": args.user_id if(args.user_type=="customer") else "",
		})

		# verify email
		if(not frappe.db.exists('Wallet', filters)):
			return create_response(NOT_FOUND, {"message": f"No wallet balance found for {filters.user_type}.", "data": filters})

		data = frappe.db.get_value("Wallet", filters, ["user_id", "user_type", "amount"], as_dict=1)
		
		
		return create_response(SUCCESS, {
			"data": data,
			"message": f"{(filters.user_type).capitalize()}, wallet balance found."
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error getting wallet balance")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def adding_transaction(args: dict):
	try:
		args = frappe._dict(args)

		# create email group member
		cargs = {
			"amount": args.amount,
			"reference": args.reference,
			"status": args.status,
			"type": args.type,
			"fromwalletid": args.fromWalletId,
			"towalletid": args.towalletid,
			"fee": args.fee,
			"description": args.description,
			"externalreference": args.externalReference,
			"paymentprovider": args.paymentProvider,
			"orderid": args.orderId,
			"releasedate": args.releaseDate,
			"email": args.email,
			"user_type": args.user_type,
			}

		# verify email
		if(frappe.db.exists('Wallet Transaction', cargs)):
			return create_response(SUCCESS, f"Already have wallet transaction.")

		cargs.update({"doctype": "Wallet Transaction"})
		
		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return create_response(SUCCESS, {
			"data": doc,
			"message": "Wallet transaction added sucessfully!"
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error creating wallet transaction")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


