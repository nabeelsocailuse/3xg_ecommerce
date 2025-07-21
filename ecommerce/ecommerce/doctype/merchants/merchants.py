# Copyright (c) 2024, 3XG and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Merchants(Document):
	def validate(self):
		self.set_full_name()

	def set_full_name(self):
		full_name = ""
		if(self.first_name): full_name += self.first_name + " "
		if(self.last_name): full_name += self.last_name
		self.full_name = full_name