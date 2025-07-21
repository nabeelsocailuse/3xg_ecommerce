# Copyright (c) 2024, 3XG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
'''from ecommerce.integrations.itranxit import (
	post_order_to_itraxit, 
	post_bulk_itraxit_orders
)'''

class Order(Document):
	def validate(self):
		self.calculate_commission()
		# self.submit_payment_entry()
		# frappe.enqueue(
		# 	make_accounting_entries,
		# 	timeout=300,
		# 	self = self,
		# 	publish_progress=False,
		# )
		# make_accounting_entries(self)
	
	def calculate_commission(self):
		total, total_commission = 0,0
		for row in self.items:
			row.commission_amount = (row.commissionpercentage/100) * row.price
			row.outstanding_amount = (row.price - row.commission_amount)
			# Totals
			total += row.price
			total_commission += row.commission_amount
		
		self.total = total + self.shipping_fee
		self.total_commission = total_commission
		self.outstanding_amount = (total -  total_commission)

	def transfer_to_merchant(self):
		if(self.status=='Completed'):
			args = get_gl_structure()
			args.update({
				'account': self.merchant_account,
				'credit': self.outstanding_amount,
				'debit': 0
			})

	def submit_payment_entry(self):
		if(self.status=='Completed'):
			doc = frappe.get_doc('Payment Entry', {'custom_order_id': self.order_id})
			if(doc.docstatus==0):
				doc.submit()
		
	def after_insert(self): 
		pass
		# post_order_to_itraxit(self)
		# post_bulk_itraxit_orders(self)
		frappe.enqueue(
			make_accounting_entries,
			timeout=300,
			self = self,
			publish_progress=False,
		)
		# self.create_sales_invoice()
		# create_sales_invoice(self)
	'''def on_trash(self):
		if(frappe.db.exists('Accounting Transactions', self.name)):
			frappe.db.sql(f"update `tab'Accounting Transactions' set voucher_no='' where voucher_no={self.name}")
			frappe.db.sql(f"delete from `tab'Accounting Transactions' where voucher_no={self.name}")'''

""" Create User with user_type = 'Website User' """
def create_sales_invoice(self, publish_progress=True):
	email = frappe.db.get_value("Website User", {"user_id": self.user_id}, "email")
	# frappe.throw(f"{email}")
	if(email):
		customer = frappe.db.get_value("Customer", {"user_id": email}, "name")
		if(customer):
			settings = frappe.get_doc('Ecommerce Settings')
			commission_rate = sum(d.commissionpercentage for d in self.items) or 0.0
			args = {
				"doctype": "Sales Invoice",
				"company": settings.company,
				"customer": customer,
				"update_stock": 0,
				"commission_rate": commission_rate,
				"set_warehouse": settings.virtual_warehouse,
				"items": [{
					"item_code": d.item_code,
					"qty": d.quantity,
					"rate": (d.price/d.quantity),
				} for d in self.items],
				# 'taxes_and_charges': get_default_Sales_Taxes_and_Charges_Template(),
				'custom_order_id' : self.order_id,
				'shipping_rule': get_shipping_rule(self, settings)
			}		
			doc = frappe.get_doc(args)
			doc.set_taxes()
			doc.insert(ignore_permissions=True)
			doc.submit()

		create_mode_of_payment(self, settings)
		create_payment_entry(self, settings, doc)

def get_default_Sales_Taxes_and_Charges_Template():
	return frappe.db.sql('''
						Select name
						From `tabSales Taxes and Charges Template`
						Where is_default=1
						Limit 1
						 ''')[0][0] or None

def get_shipping_rule(self, settings):
	label_name = f'Shipping Fee {self.name}'
	if(frappe.db.exists('Shipping Rule', label_name)):
		return label_name

	args = frappe._dict({
		'doctype': 'Shipping Rule',
		'label': label_name,		
		'shipping_rule_type': 'Selling',
		'company': settings.company,
		'account': settings.shipping_account,
		'cost_center': frappe.get_cached_value("Company", settings.company, "cost_center"),
		'calculate_based_on': 'Fixed',
		'shipping_amount': self.shipping_fee,
		'countries': [{
			'country': 'Nigeria'
		}]
	})
	doc = frappe.get_doc(args)
	doc.insert(ignore_permissions=True)
	
	return doc.name

def create_mode_of_payment(self, settings):
	if(not frappe.db.exists('Mode of Payment', self.payment_method)):
		args = frappe._dict({
			'doctype': 'Mode of Payment',
			'mode_of_payment': self.payment_method,		
			'enabled': 1,
			'type': "Cash",
			'accounts':  [{
				'company': settings.company,
				'default_account': settings.wallet_account,
			}]
		})
		doc = frappe.get_doc(args)
		doc.insert(ignore_permissions=True)
	else:

		doc = frappe.get_doc('Mode of Payment', self.payment_method)
		is_not_exists = True
		
		for row in doc.accounts:
			if(row.company == settings.company): is_not_exists = False
		
		if(is_not_exists):
			doc.append('accounts', {
							'company': settings.company,
							'default_account': settings.wallet_account,
						})
			doc.save(ignore_permissions=True)

def create_payment_entry(self, settings, doc):
	args = frappe._dict({
		'doctype': 'Payment Entry',
		'payment_type': 'Receive',		
		'mode_of_payment': self.payment_method,
		'custom_order_id': self.order_id,
		'company': settings.company,
		'party_type': "Customer",
		'party': doc.customer,
		'paid_to': settings.wallet_account,
		'paid_amount': doc.outstanding_amount,
		'received_amount': doc.outstanding_amount,
		'target_exchange_rate': 1,
		'references': [{
			'reference_doctype': 'Sales Invoice',
			'reference_name': doc.name,
			'allocated_amount': doc.outstanding_amount
		}]
	})
	doc = frappe.get_doc(args)
	doc.flags.ignore_mandatory=True
	doc.insert(ignore_permissions=True)

"""
def get_itraxit_order():
	import requests
	# Define the API endpoint
	order_id = "9e092b48-0aac-47fe-b58c-69f669d0383a"
	url = f"https://backend.itranxit.com/api/v1/external/order/{order_id}"
	# Define the API key and its value
	headers = {
		"x-api-key": "qtAPTvoifLWxAoTn",  # Replace with your actual API key
		"Content-Type": "application/json"  # Ensure the content type is JSON
	}
	body={
		
	}
	# Make the GET request
	response = requests.get(url, headers=headers, json=body)
	# Check the response
	if response.status_code == 200 or response.status_code == 201:
		print("Order found successfully:", response.json())
	else:
		print("Failed to get order:", response.status_code, response.text)

def get_all_itraxit_orders():
	import requests
	# Define the API endpoint
	order_id = "9e092b48-0aac-47fe-b58c-69f669d0383a"
	url = f"https://backend.itranxit.com/api/v1/external/order/index?limit=5"
	# Define the API key and its value
	headers = {
		"x-api-key": "qtAPTvoifLWxAoTn",  # Replace with your actual API key
		"Content-Type": "application/json"  # Ensure the content type is JSON
	}
	body={
		
	}
	# Make the GET request
	response = requests.get(url, headers=headers, json=body)
	# Check the response
	if response.status_code == 200 or response.status_code == 201:
		print("Order found successfully:", response.json())
	else:
		print("Failed to get order:", response.status_code, response.text)

 
{
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
	  // Merchant Information
	  "pickup_address":"29 Handsdown Street Ikeja Lagos",
	  "pickup_coordinate":"None",
	  "dropoff_coordinate":"None",
	  "pickup_phone":"08025467892",
	  // Merchant Information
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
}
"""

def get_gl_structure(self):
	return frappe._dict({
		'doctype': 'Accounting Transactions',
		'posting_date': getdate(),
		'party_type': 'Website User',
		'party': self.email,
		'against': 'Order',
		'voucher_type': 'Order',
		'voucher_no': self.name,
		'remarks': 'Order received',
		'company': self.company,
		'due_date': getdate(),
		'is_cancelled': 0,
	})
# Make GL Entries
def make_accounting_entries(self, publish_progress=False):
	args = get_gl_structure(self)

	# # Debit To Account Entry
	# args.update({
	# 	'account': self.debit_to_account,
	# 	'debit': self.total,
	# 	'credit': 0
	# })
	# frappe.get_doc(args).insert(ignore_permissions=True)

	# Wallet Account Entry
	args.update({
		'account': self.wallet_account, 
		'debit': self.total,
		'credit': 0,
	})
	frappe.get_doc(args).insert(ignore_permissions=True)

	# Shpping Account Entry
	args.update({
		'account': self.shipping_account,
		'debit': 0,
		'credit': self.shipping_fee,
	})
	frappe.get_doc(args).insert(ignore_permissions=True)

	# Merchant Account Entry
	args.update({
		'account': self.merchant_account,
		'debit': 0,
		'credit': self.outstanding_amount
	})
	frappe.get_doc(args).insert(ignore_permissions=True)

	# company commission account entry
	for row in self.items:
		args.update({
			'party_type': 'Merchants',
			'party': row.seller_id,
			'item_code': row.item_code,
			'account': self.commission_account,
			'debit': 0,
			'credit': row.commission_amount
		})
		frappe.get_doc(args).insert(ignore_permissions=True)

