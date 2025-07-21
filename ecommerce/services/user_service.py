import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

def list_users():
	try:
		query = """
			SELECT *
			FROM `tabWebsite User`
			WHERE 1=1
		"""
		
		users = frappe.db.sql(query, as_dict=True)

		if not users:
			return create_response(NOT_FOUND, [])

		return create_response(SUCCESS, users)

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching users")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

# def create_user(user_id, username, email, password_hash, password_salt):
def creating_user(args: dict):
	try:
		args = frappe._dict(args)
		if(frappe.db.exists("Website User", args.email)):
			return create_response(SUCCESS, {
				"message": "User already exists.",
				"data": args.email
			})

		cargs = {
			"user_id": args.user_id,
			"username": args.username,
			"email": args.email,
			"password_hash": args.password_hash,
			"password_salt": args.password_salt,
			"last_name": args.lastname,
			"first_name": args.firstname,
			"middle_name": args.middlename,
			"gender": args.gender,
			"phone": args.phone,
			"isverified": args.isVerified,
			"doctype": "Website User"
		}
		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return create_response(SUCCESS, {
			"message": "User created successfully.",
			"data": doc
		})

	except ValueError as e:
		frappe.log_error(f"Data validation error for user: {str(e)}", "User Creation Validation Error")
		return create_response(BAD_REQUEST, f"Validation error: {str(e)}")

	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error for user: {str(e)}", "User Creation Validation Error")
		return create_response(BAD_REQUEST, f"Frappe validation error: {str(e)}")

	except Exception as e:
		frappe.log_error(f"Error creating user for user: {str(e)}", "User Creation Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
	
# def update_user_by_id(user_id, username, product_name=None, category=None, actual_price=None, discounted_price=None, image=None, rating=None, brand=None, description=None, product_line=None, model=None, weight=None, availability=None, color=None, quantity=None, warranty=None, collection=None):
def updating_user(args: dict):
	try:
		args = frappe._dict(args)
		doc = frappe.get_doc("Website User", args.email)
		if(not doc):
			raise frappe.DoesNotExistError(f"User with <b>{args.email}</b> not found!")

		doc.username = args.username
		doc.first_name = args.firstname
		doc.middle_name = args.middlename
		doc.last_name = args.lastname
		doc.gender = args.gender
		doc.phone = args.phone
		doc.password_hash = args.password_hash
		doc.password_salt = args.password_salt
		doc.isverified = args.isVerified
		doc.save(ignore_permissions=True)
		frappe.db.commit()

		return create_response(SUCCESS, f"User {args.email} updated successfully!")
	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title=f"Error updating item {args.email}")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def verifying_user(args: dict):
	args = frappe._dict(args)
	try:
		doc = frappe.get_doc("Website User", args.email)
		if(not doc):
			raise frappe.DoesNotExistError(f"User with <b>{args.email}</b> not found!")
		
		doc.isverified = args.isVerified
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return create_response(SUCCESS, f"User {args.email} verified successfully!")
	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title=f"Error updating item {args.email}")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
