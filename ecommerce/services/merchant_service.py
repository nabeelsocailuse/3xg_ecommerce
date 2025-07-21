import frappe, json
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_merchants():
   
	try:
		query = """
			SELECT *
			FROM `tabMerchants`
			WHERE 1=1
		"""
		 
		merchants = frappe.db.sql(query, as_dict=True)

		if not merchants:
			return create_response(NOT_FOUND, [])

		return create_response(SUCCESS, merchants)

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching merchants")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def get_merchant_by_id(merchant_id):
	try:
		query = """
			SELECT *
			FROM `tabMerchants`
			WHERE merchant_id = %s
		"""
		
		merchant = frappe.db.sql(query, (merchant_id,), as_dict=True)

		if not merchant:
			return create_response(NOT_FOUND, [])

		return create_response(SUCCESS, {
			"message": "Merchant fetched successfully.",
			"data": merchant[0] 
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching merchant by ID")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

### Add new item
def add_new_merchant(merchant_id, username, email, password, phone, business_name, business_type, business_category, business_address, business_location_lat, business_location_long, first_name=None, last_name=None,  role=None, street=None, city=None, state=None, country=None):
	
	try:
		if frappe.db.exists("Merchants", {"merchant_id": merchant_id}):
			raise ValueError(f"Merchant with code '{merchant_id}' already exists!")

		def validate_bussiness_type():
			if(frappe.db.exists('Business Type', business_type)):
				pass
			else:
				doc = frappe.new_doc('Business Type')
				doc.business_type_name = business_type
				doc.insert(ignore_permissions=True)
			
		def create_business_category(category):
			doc = frappe.new_doc('Business Category')
			doc.category_name = category
			doc.business_type = business_type
			doc.insert(ignore_permissions=True)
			return doc.name
		
		def get_business_category():
			if(type(business_category)==list):
				bclist = []
				for category in business_category:
					category = category if(frappe.db.exists('Business Category', category)) else create_business_category(category)
					bclist.append({'business_category': category})    
				return bclist
			raise ValueError(f"Business category must be in form of list.")
		
		validate_bussiness_type()
		
		new_item = frappe.get_doc({
			"doctype": "Merchants",
			"merchant_id": merchant_id,
			"first_name": first_name,
			"last_name": last_name,
			"username": username,
			"email": email,
			"password": password,
			"phone": phone,
			"role": role,
			"business_name": business_name,
			"business_type": business_type,
			# "business_category": business_category,
			"business_categories": get_business_category(),
			"business_address": business_address,
			"business_location_lat": business_location_lat,
			"business_location_long": business_location_long,
			"street": street,
			"city": city,
			"state": state,
			"country": country,
		})
		new_item.insert(ignore_permissions=True)
		frappe.db.commit()

		return create_response(SUCCESS, f"Merchant '{merchant_id}' added successfully!")

	except ValueError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(f"Error adding new merchant '{merchant_id}': {str(e)}", "Add Merchant Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

@frappe.whitelist(allow_guest=True)
def calculate_merchant_performance(user_id, seller_id):
	
	try:
		if(frappe.db.exists("User", user_id)):
			data = frappe.db.sql(""" 
				Select 
					idt.seller_id, idt.seller_name, sum(idt.quantity) as selling_qty,  
					(Select sum(quantity) as actual_qty From `tabProducts` Where docstatus=0 and merchant_id = idt.seller_id) as actual_qty
				From 
					`tabOrder` odr inner join `tabOrder Item` idt on (odr.name=idt.parent)
				Where 
					odr.docstatus=0 
					and idt.seller_id = %(seller_id)s
				""", {"seller_id": seller_id}, 
				as_dict=True)
			
			performance_dict= {}
			for d in data:
				performance_dict.update({
					"seller_name": d.seller_name, 
					"percentage": round((d.selling_qty/d.actual_qty) * 100, 2) 
				})
			return create_response(SUCCESS, {"message": "Seller performance found.", "data": performance_dict})
		else:
			return create_response(NOT_FOUND, {"message": "User not found.", "data": []})
	except Exception as e:
		return create_response(SERVER_ERROR, f"{e}")


def get_merchant_balances():
	try:
		query = """
			SELECT
				name AS merchant_id,
				name,
				amount
			FROM `tabWallet`
			WHERE 1=1
		"""

		merchants = frappe.db.sql(query, as_dict=True)

		if not merchants:
			return create_response(NOT_FOUND, [])

		return create_response(SUCCESS, merchants)

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching merchant balances")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
