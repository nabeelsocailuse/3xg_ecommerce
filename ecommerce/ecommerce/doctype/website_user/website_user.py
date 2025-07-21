# Copyright (c) 2024, 3XG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WebsiteUser(Document):
	def after_insert(self):
		# self.create_user()
		self.create_customer()

	""" Create User with user_type = 'Website User' """
	def create_user(self):
		if(frappe.db.exists("User", self.email)): 
			return 
		frappe.get_doc({
			"doctype": "User",
			"email": self.email,
			"first_name": self.first_name,
			"middle_name": self.middle_name,
			"last_name": self.last_name,
			"username": self.username,
			"gender": self.gender,
			"phone": self.phone,
			"send_welcome_email": 0,
		}).save(ignore_permissions=True)

	""" Create Customer linked with User """
	def create_customer(self):
		if(frappe.db.exists("Customer", {"user_id": self.email})): 
			return
		# if(frappe.db.exists("Website User", self.email)):
		customer_name = []
		if(self.first_name): customer_name.append(self.first_name)
		if(self.middle_name): customer_name.append(self.middle_name)
		if(self.last_name): customer_name.append(self.last_name)
		if(not customer_name): customer_name.append(str(self.email).split("@")[0])
		frappe.get_doc({
			"doctype": "Customer",
			"user_id": self.email,
			"customer_name": " ".join(customer_name),
			"customer_group": "Individual",
			"territory": "All Territories",
		}).save(ignore_permissions=True)

	def on_trash(self):
		if(frappe.db.exists("Customer", {"user_id": self.email})):
			frappe.delete_doc("Customer", {"user_id": self.email})
		if(frappe.db.exists("User", self.email)):
			frappe.delete_doc("User", self.email)