import frappe, requests

# Define the API key and its value
headers = {
    "x-api-key": "qtAPTvoifLWxAoTn",  # Replace with your actual API key
    "Content-Type": "application/json"  # Ensure the content type is JSON
}

def post_order_to_itraxit(self):
    def get_receiver_info(user_id):
        data = frappe.db.get_value("Website User", {"user_id": user_id}, "*", as_dict=1)
        
        fullname = [data.first_name or "", data.middle_name or "", data.last_name or ""]
        fullname = " ".join(fullname) if(fullname) else ""
        return {
            "receiver_name": fullname,
            "receiver_phone": data.phone or "-",
        }
    
    def get_merchant_info(merchant_id):
        data = frappe.db.get_value("Merchants", merchant_id, "*", as_dict=1)
        addresslist = []
        if(data.street): addresslist += [data.street]
        if(data.city): addresslist += [data.city]
        if(data.state): addresslist += [data.state]
        if(data.country): addresslist += [data.country]
        
        pickup_address = " ".join(addresslist) if(addresslist) else ""
        return {
            "pickup_address": pickup_address,
            "pickup_phone": data.phone or "-",
            "state_id": data.state,  # Lagos
            "country_id": data.country,  # Nigeria
        }
        
    def processing_order():
        body = {}
        rbody = get_receiver_info(self.user_id)
        body.update(rbody)
        for row in self.items:
            mbody = get_merchant_info(row.seller_id)
            body.update(mbody)
            body.update({
                "parcel_name": row.item_name,
                "description": f"{row.item_code} {row.item_name}",
                "distance_to_destination": 106,  # in Km
                "dropoff_address": self.shipping_address,
                "country_id": 160, 
                "state_id": 2671
            })
            post_order(body)
            
    def post_order(body):
        # Define the API endpoint
        url = "https://backend.itranxit.com/api/v1/external/order/create"
        # Make the POST request
        response = requests.post(url, headers=headers, json=body)
        # Check the response
        print("-----------------")
        print("response: ", response)
        if response.status_code == 200 or response.status_code == 201:
            print("Order created successfully:", response.json())
            save_itranxit_info(self.name, response.json())
        else:
            print("Failed to create order:", response.status_code, response.text)

    processing_order()

def save_itranxit_info(name, result):
    data = frappe._dict(result)
    orderObj = frappe._dict(data["order"])
    
    # start: setup customer details 
    customerObj = frappe._dict(orderObj["customer"])
    customerObj.update({
        "customer_status": customerObj.pop("status"),
    })
    orderObj.update(customerObj)
    # end: setup customer details
    
    # start: setup profile details 
    profileObj = frappe._dict(customerObj["profile"])
    profileObj.update({
        "customerid": profileObj.pop("customerID"),
        "userid": profileObj.pop("userID")
    })
    orderObj.update(profileObj)
    # end: setup profile details 
    
    # start: setup wallet details 
    walletObj = frappe._dict(customerObj["wallet"])
    orderObj.update(walletObj)
    # end: setup wallet details
    
    # start: setup bank details 
    bankObj = frappe._dict(customerObj["bank"])
    profileObj.update({
        "bank_type": bankObj.pop("type"),
    })
    orderObj.update(bankObj)
    # end: setup bank details
    
    # Now insert into database...
    orderObj.update({
        "doctype": "iTranxit Tracker",
        "orderid": orderObj.pop("orderID"),
        "ordercode": orderObj.pop("orderCode"),
        "order": name,
        
    })
    # frappe.msgprint(frappe.as_json(orderObj))
    doc = frappe.get_doc(orderObj)
    doc.insert(ignore_permissions=True)
    
# bench --site 3xg.africa execute ecommerce.ecommerce.doctype.order.order.make_itraxit_order
def post_bulk_itraxit_orders(self):
	def get_receiver_info(user_id):
		data = frappe.db.get_value("Website User", {"user_id": user_id}, "*", as_dict=1)
		
		fullname = [data.first_name or "", data.middle_name or "", data.last_name or ""]
		fullname = " ".join(fullname)
		return {
			"receiver_name": fullname,
			"receiver_phone": data.phone or "-",
			"receiver_address": self.shipping_address, 
		}

	def get_merchant_info(merchant_id):
		data = frappe.db.get_value("Merchants", merchant_id, "*", as_dict=1)
		addresslist = [data.street, data.city, data.state, data.country]
		pickup_address = " ".join(addresslist)
		return {
			"pickup_address": pickup_address,
			"pickup_phone": data.phone or "-",
		}

	def create_orders():
		# Define the request body
		rbody = get_receiver_info(self.user_id)
		orders_list = []
		for row in self.items:
			cbody = {}
			cbody.update(rbody)
			mbody = get_merchant_info(row.seller_id)
			cbody.update(mbody)
			cbody.update({
				"parcel_name": row.item_name,
				"description": f"{row.item_code} {row.item_name}",
				"distance_to_destination": 106,  # in Km
			})
			orders_list.append(cbody)

		if(orders_list):
			body = {
				"country_id": 160, 
				"state_id": 2671,
			}
			
			body.update(rbody)
			body.update({"orders": orders_list})
			# frappe.throw(f"{body}")
			post_bulk_orders(body)

	def post_bulk_orders(body):
		url = "https://backend.itranxit.com/api/v1/external/order/bulk/create"
		# Make the POST request
		response = requests.post(url, headers=headers, json=body)
		# Check the response
		print("-----------------")
		print("response: ", response)
		if response.status_code == 200 or response.status_code == 201:
			print("Order created successfully:", response.json())
			save_itranxit_info(response.json())
		else:
			print("Failed to create order:", response.status_code, response.text)

	create_orders()
	""" body = {
	"orders": [
			{
				"parcel_name": "Hand Bag",
				"pickup_address": "20 Shodipo Close Abule Egba Lagos",
				"pickup_phone": "09090876784",
				"receiver_name": "Abass Paul",
				"receiver_address": "29 Handsdown Street Ikeja Lagos",
				"receiver_phone": "08025467892",
				"distance_to_destination": 90
			},
			{
				"parcel_name": "Phone Charger",
				"pickup_address": "98 Chief Olise Street Ojota Lagos",
				"pickup_phone": "08078789878",
				"receiver_address": "45 Baton Exchange Street Lekki Lagos",
				"receiver_phone": "09089098900",
				"receiver_name": "Sarah Smith",
				"distance_to_destination": 120
			},
			{
				"parcel_name": "Candy Crush",
				"pickup_address": "45 Yvonne Street Ogba Lagos",
				"pickup_phone": "08078789878",
				"receiver_address": "12 Candy Crush Street Ketu Lagos",
				"receiver_phone": "07076453789",
				"receiver_name": "Peter Nwakaego",
				"distance_to_destination": 130
			}
		],
		"country_id": 160, 
		"state_id": 2671 
	} """

""" {
"message":"Order created successfully",
"order":{
    "orderID":"9e092b48-0aac-47fe-b58c-69f669d0383a",
    "orderCode":86310194,
    "is_bulk":false,
    "bulk_order_id":"None",
    "amount":11400,
    "original_amount":"None",
    "amount_paid":"None",
    "parcel_name":"Hand Bag",
    "category":"None",
    "vehicle_type":"None",
    "description":"This order is coming from the 3xg application",
    "schedule_for":"now",
    "schedule_date_time":"None",
    "country":"Nigeria",
    "state":"Lagos",
    #  Merchant Information
    "pickup_address":"29 Handsdown Street Ikeja Lagos",
    "pickup_coordinate":"None",
    "dropoff_coordinate":"None",
    "pickup_phone":"08025467892",
    #  Merchant Information
    "pickup_at":"None",
    "pickup_code":"None",
    "accepted_at":"None",
    "rejected_at":"None",
    "cancelled_at":"None",
    "dropped_off_at":"None",
    "driver_selected_at":"None",
    "distance_to_destination":110,
    "receiver_name":"3xg Operations Officer",
    "receiver_address":"None",
    "receiver_phone":"09090876784",
    "delivery_note":"None",
    "status":"None",
    "cancelled_by":"None",
    "payment_method":"None",
    "is_paid":false,
    "customer":{
        "id":"9e032c44-6ea2-44a2-b44e-934821bc2c55",
        "f_name":"3XG",
        "l_name":"Admin",
        "phone":"08078603426",
        "email":"support@3xg.africa",
        "address":"12 Ovba Street Ketu Lagos",
        "role":"customer",
        "image":"None",
        "ref_code":"3XGYDAPFQ",
        "email_verified_at":"None",
        "status":true,
        "profile":{
            "customerID":"9e032c44-718e-4000-93c6-7dfa2c2bae4e",
            "userID":"9e032c44-6ea2-44a2-b44e-934821bc2c55",
            "type":"business",
            "dateCreated":"2025-01-20T09:17:27.000000Z",
            "business_name":"3xg Application",
            "position":"Operations Officer",
            "business_address":"12 Ovba Street Ketu Lagos",
            "industry":"Ecommerce",
            "apikey":"qtAPTvoifLWxAoTn",
            "daily_average_orders":100,
            "order_slots_left":0,
            "is_subscribed":false,
            "plan_id":"None"
        },
        "wallet":{
            "id":"9e032c44-72f7-4afa-af02-4a38e96fab02",
            "user_id":"9e032c44-6ea2-44a2-b44e-934821bc2c55",
            "escrow_amount":"0",
            "withdrawable_amount":"0",
            "referral_balance":"0"
        },
        "bank":{
            "id":"9e032c44-747a-40d5-ac12-ef97bf80c97a",
            "user_id":"9e032c44-6ea2-44a2-b44e-934821bc2c55",
            "bank_id":"None",
            "bank_name":"None",
            "account_name":"None",
            "account_number":"None",
            "receipient_code":"None",
            "type":"None"
        },
        "dateCreated":"2025-01-20T09:17:27.000000Z"
    },
    "driver":"None",
    "created_at":"2025-01-23T08:49:40.000000Z",
    "tracking_code":"ORDER-01-2025-00031",
}
} """
    