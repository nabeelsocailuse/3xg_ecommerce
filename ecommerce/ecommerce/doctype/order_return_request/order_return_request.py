# Copyright (c) 2025, 3XG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OrderReturnRequest(Document):
	pass
	# def validate(self):
	# 	self.create_sales_return()
	# def create_sales_return(self):
	# 	doc = frappe.get_doc('Sales Invoice', {'custom_order_id': self.orderid, 'is_return': 0, 'docstatus': 1})
	# 	frappe.throw(frappe.as_json(doc))
