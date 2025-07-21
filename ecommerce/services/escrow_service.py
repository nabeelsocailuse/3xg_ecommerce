import frappe
from ecommerce.constants.http_status import (SUCCESS, NOT_FOUND, SERVER_ERROR)
from ecommerce.utils.response_helper import create_response
from frappe.core.doctype.communication.email import make

# 04-04-2025 Nabeel Saleem
def adding(args: dict):
	try:
		args = frappe._dict(args)

		cargs = {
			"merchant_id": args.merchant_id,
			"order_id": args.order_id,
			"status": args.status,
			"release_date": args.release_date,
			"total_amount": args.total_amount,
			"doctype": "Escrow"
		}
		# # verify email
		# if(frappe.db.exists('Email Group Member', {"email_group": "3xg Shop Waitlist", "email": args.email})):
		# 	return create_response(SUCCESS, f"Already in waitlist <b>{args.email}</b>")
		
		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)
		
		return create_response(SUCCESS, {
			"data": doc,
			"message": "Escrow detail added successfully!"
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error creating Escrow")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def updating(args: dict):
	try:
		args = frappe._dict(args)
		# # verify email
		# if(frappe.db.exists('Email Group Member', {"email_group": "3xg Shop Waitlist", "email": args.email})):
		# 	return create_response(SUCCESS, f"Already in waitlist <b>{args.email}</b>")
		
		doc = frappe.get_doc("Escrow", {
			"merchant_id": args.merchant_id,
			"order_id": args.order_id
			})
		doc.status = args.status
		doc.release_date = args.release_date
		doc.total_amount = args.total_amount
		doc.save(ignore_permissions=True)
		
		return create_response(SUCCESS, {
			"data": doc,
			"message": "Escrow detail updated successfully!"
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error updating Escrow")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
