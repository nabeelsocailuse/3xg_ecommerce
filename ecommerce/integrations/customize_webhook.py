import frappe, requests

# Define the API key and its value
headers = {
	# "x-api-key": "qtAPTvoifLWxAoTn",  # Replace with your actual API key
	"Content-Type": "application/json"  # Ensure the content type is JSON
}

url = "https://dev-api1.3xg.africa/api/webhooks/erp-next"


def send_coupon_code_info(doc, method=None):
	
	body = {
		"event": "coupon.created" if(doc.is_new()) else "coupon.updated",
		"data": {
			"coupon_type": doc.coupon_type,
			"coupon_name": doc.coupon_name,
			"coupon_code": doc.coupon_code,
			"description": doc.description,
			"maximum_use": doc.maximum_use,
			"used": doc.used,
			"valid_from": doc.valid_from,
			"valid_upto": doc.valid_upto,
			"pricing_rule": {
			"id": doc.pricing_rule,
			"items": get_pricing_rule(doc)
			},
			"discount_percentage": doc.discount_percentage,
			"discount_amount": doc.discount_amount
		}
	} 
	print(body)
	response = requests.post(url, headers=headers, json=body)
	# Check the response
	print("-----------------")
	print("response: ", response)
	if response.status_code == 200 or response.status_code == 201:
		print("Order created successfully:", response.json())
	#   save_itranxit_info(self.name, response.json())
	else:
		print("Failed to create order:", response.status_code, response.text)
		# frappe.log_error(f"Failed to send coupon code info: {response.status_code} {response.text}")
	doc = frappe.new_doc("Webhook Request Log")
	doc.user= frappe.session.user
	doc.headers= frappe.as_json({"Content-Type": "application/json"})
	doc.data= frappe.as_json(body)
	doc.url= url
	doc.response= frappe.as_json(response)
	doc.response= frappe.as_json(response.text)
	doc.save(ignore_permissions=True)

def get_pricing_rule(doc):
	if(doc.apply_on == "Item Code"):
		return frappe.db.sql(f"""
			Select 
				itm.item_code, itm.merchant, pr.uom 
			From 
				`tabItem` itm inner join `tabPricing Rule Item Code` pr on (itm.name=pr.item_code)
			Where 
				parent = '{doc.pricing_rule}'
			""", as_dict=1)

	elif(doc.apply_on == "Item Group"):
		return frappe.db.sql(f"""
			Select 
				itm.item_code,  itm.merchant, pr.uom 
			From 
				`tabItem` itm inner join `tabPricing Rule Item Group` pr on (itm.item_group=pr.item_group)
			Where 
				parent = '{doc.pricing_rule}'
			Group By
				itm.item_code
			""", as_dict=1)

	elif(doc.apply_on == "Brand"):
		return frappe.db.sql(f"""
			Select 
				itm.item_code, itm.merchant, pr.uom 
			From 
				`tabItem` itm inner join `tabPricing Rule Brand` pr on (itm.brand=pr.brand)
			Where 
				parent = '{doc.pricing_rule}'
			Group By
				itm.item_code
			""", as_dict=1)
	return []


def send_home_banners_to_node(doc, method=None):
	from ecommerce.services.banners_service import get_home_banners
	try:
		banners = get_home_banners({})

		body = {
			"event": "home_banners.updated",
			"data": banners
		}
		response = requests.post(url, headers=headers, json=body)
		# Check the response
		print("-----------------")
		print("response: ", response)
		if response.status_code == 200 or response.status_code == 201:
			print("Order created successfully:", response.json())
		#   save_itranxit_info(self.name, response.json())
		else:
			print("Failed to create order:", response.status_code, response.text)
			# frappe.log_error(f"Failed to send coupon code info: {response.status_code} {response.text}")
		doc = frappe.new_doc("Webhook Request Log")
		doc.user= frappe.session.user
		doc.headers= frappe.as_json({"Content-Type": "application/json"})
		doc.data= frappe.as_json(body)
		doc.url= url
		doc.response= frappe.as_json(response)
		doc.response= frappe.as_json(response.text)
		doc.save(ignore_permissions=True)
		
	except ValueError as e:
		frappe.log_error(f"Data validation error", "Home Banners error")
	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error: {str(e)}", "Home Banners error")
	except Exception as e:
		frappe.log_error(f"Error creating Home Banners: {str(e)}", "Home Banners error")
		
