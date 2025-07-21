import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

def add_bank_account(args: dict):
	try:
		args = frappe._dict(args)
		
		cargs = frappe._dict({
			'doctype': "BankAccount",
			'accountname': args.accountName,
			'accountnumber': args.accountNumber,
			'bankcode': args.bankCode,
			'bankname': args.bankName,
			'merchantid': args.merchantId,
			'isdefault': args.isDefault
		})
		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return create_response(SUCCESS, {"data": doc})

	except ValueError as e:
		frappe.log_error(f"Data validation error", "BankAccount error")
		return create_response(BAD_REQUEST, {"message": f"Validation error: {str(e)}"})
	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error: {str(e)}", "BankAccount error")
		return create_response(BAD_REQUEST, {"message": f"Frappe validation error: {str(e)}"})
	except Exception as e:
		frappe.log_error(f"Error creating BankAccount: {str(e)}", "BankAccount error")
		return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})

def get_bank_account(args: dict):
	try:
		filters = frappe._dict(args)
		conditions = get_conditions(filters)
		data = frappe.db.sql('''
                Select * 
                From `tabBankAccount`
                Where docstatus=0
                %s
                '''%conditions, filters, as_dict=1)
		return create_response(SUCCESS, {"data": data})

	except ValueError as e:
		frappe.log_error(f"Data validation error", "BankAccount error")
		return create_response(BAD_REQUEST, {"message": f"Validation error: {str(e)}"})
	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error: {str(e)}", "BankAccount error")
		return create_response(BAD_REQUEST, {"message": f"Frappe validation error: {str(e)}"})
	except Exception as e:
		frappe.log_error(f"Error creating BankAccount: {str(e)}", "BankAccount error")
		return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})

def get_conditions(filters):
	conditions = " and accountname=%(accountName)s " if(filters.get("accountName")) else ""
	conditions += " and accountnumber=%(accountNumber)s " if(filters.get("accountNumber")) else ""
	conditions += " and bankcode=%(bankCode)s " if(filters.get("bankCode")) else ""
	conditions += " and bankname=%(bankName)s " if(filters.get("bankName")) else ""
	conditions += " and merchantid=%(merchantId)s " if(filters.get("merchantId")) else ""
	conditions += " and isdefault=%(isDefault)s " if(filters.get("isDefault")) else ""
	return conditions
