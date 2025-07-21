# Copyright (c) 2024, 3XG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from nanoid import generate
# from erpnext import get_default_company

class Products(Document):
	def validate(self):
		
		# self.create_item()
		# self.create_item_price()
		# self.create_stock_entry()
		# frappe.enqueue(
		# 	process_item_creation,
		# 	timeout=300,
		# 	self = self,
		# 	publish_progress=False,
		# )
		self.generate_sku()
		if(self.name != self.item_code):
			frappe.enqueue(
				rename_product,
				timeout=300,
				self = self,
				publish_progress=False,
			)
	# def after_insert(self):
	# 	self.rename_product()

	def generate_sku(self):
		if(not self.item_code):
			sku_no = generate("0123456789", 10)
			self.sku = sku_no
			self.item_code = sku_no
	
	def on_trash(self):
		
		def delete_stock_entry():
			items ={	
				"t_warehouse": "Merchant Warehouse - 11",
				"item_code": self.item_code,
				"qty": self.quantity,
			}

			stock_entry = frappe.db.get_value("Stock Entry Detail", items, "parent")
			if(stock_entry):
				frappe.delete_doc("Stock Entry", stock_entry)
		
		def delete_item():
			if(frappe.db.exists("Item", self.item_code)):
				frappe.delete_doc("Item", self.item_code)
		
		def delete_item_price():
			item_price = frappe.db.get_value("Item Price", {"item_code": self.item_code}, "name")
			if(item_price):
				frappe.delete_doc("Item Price", item_price)

		delete_stock_entry()
		delete_item_price()		
		delete_item()

def rename_product(self, publish_progress=False,):
	frappe.rename_doc('Products', self.name, self.item_code, merge=False)


def process_item_creation(self, publish_progress=True):
	create_item(self)
	create_item_price(self)
	# create_stock_entry(self)

def create_item(self):
	
	args ={
		"doctype": "Item",
		"item_code": self.item_code,
		"item_name": self.product_name,
		"description": self.description,
		"item_group": get_item_group(self.category),
		"sub_item_group": get_item_group(self.sub_category),
		"sub_sub_item_group": get_item_group(self.sub_sub_category),
		"brand": get_brand(self.brand),
		"max_discount": self.discount,
		"disabled": self.is_disabled,
		"publish": self.is_live,
		# "is_stock_item": 1,
		"valuation_rate": self.actual_price,
		"item_defaults": [{"company": "3xgAfrica", "default_warehouse": "Merchant Virtual Warehouse (MVW) - 11"}],
		"merchant": self.merchant_id,
		# Features
		"model": self.model,
		"collection": self.collection,
		"weight": self.weight,
		"rating": self.rating,
		"model": self.model,
		# Specifications
		"specifications": [{"key": d.key, 'value': d.value} for d in self.specifications],
		# Colors Info
		"color": [{"color": d.color} for d in self.color],
		"warranty": self.warranty,
		"key_features": self.key_features,
		"grant_commission": 1,
		"commissionpercentage": self.commissionpercentage,
		"commission": self.commission,
		"standard_rate": self.actual_price
	}
	
	
	if(self.item_code):
		if(frappe.db.exists("Item", self.item_code)):
			doc  = frappe.get_doc("Item", self.item_code)
			doc.item_code = self.sku
			doc.item_name = self.product_name
			doc.description = self.description
			doc.item_group = get_item_group(self.category)
			doc.brand = self.brand
			doc.valuation_rate = self.actual_price
			doc.disabled = self.is_disabled
			doc.publish =  self.is_live
			# Features
			doc.model = self.model
			doc.collection = self.collection
			doc.weight = self.weight
			doc.rating = self.rating
			# Specifications
			doc.set("specifications", [{"key": d.key, 'value': d.value} for d in self.specifications])
			# Colors Info
			doc.set("color",[{"color": d.color} for d in self.color])
			doc.warranty = self.warranty
			doc.key_features = self.key_features
			doc.grant_commission = 1,
			doc.commissionpercentage =  self.commissionpercentage,
			doc.commission =  self.commission,
			# Save
			doc.save(ignore_permissions=True)
		else:
			doc = frappe.get_doc(args).insert(ignore_permissions=True)
	else:
		doc = frappe.get_doc(args).insert(ignore_permissions=True)
	
def create_item_price(self):
	args ={
		"doctype": "Item Price",
		"item_code": self.item_code,
		"item_name": self.product_name,
		"price_list": "Standard Selling",
		"selling": 1,
	}
	rate = self.discounted_price if((self.discounted_price or 0)>0) else self.actual_price
	if(frappe.db.exists(args)):

		args.update({
			"price_list_rate": rate,
		})
		if(not frappe.db.exists(args)):
			doc = frappe.get_doc("Item Price", {"item_code": self.item_code})
			doc.price_list_rate = rate
			doc.save(ignore_permissions=True)
	else:
		args.update({
			"item_description": self.description,
			"price_list_rate": rate,
		})
		frappe.get_doc(args).insert(ignore_permissions=True)
	
def create_stock_entry(self):
	items ={	
		"t_warehouse": "Merchant Virtual Warehouse (MVW) - 11",
		"item_code": self.item_code,
		"docstatus": ["<", 2]
	}
	stock_entry = frappe.db.get_value("Stock Entry Detail", items, ["name", "parent"], as_dict=1)
	
	if(self.status in ["LIVE"]):
		if(stock_entry):
			frappe.db.set_value("Stock Entry Detail", stock_entry.name, "qty", self.quantity)
			frappe.db.set_value("Stock Ledger Entry", {"voucher_no": stock_entry.parent}, "actual_qty", self.quantity)
			frappe.db.set_value("Bin", {"item_code": self.item_code}, "actual_qty", self.quantity)
		else:
			items.pop("docstatus")
			items.update({"qty": self.quantity})
			args = {
				"doctype": "Stock Entry",
				"company": "3xgAfrica",
				"stock_entry_type": "Material Receipt",
				"to_warehouse": "Merchant Virtual Warehouse (MVW) - 11",
				"items": [items],
				"merchant": self.merchant_id
			}
			doc = frappe.get_doc(args)
			doc.insert(ignore_permissions=True)
			doc.submit()
	else:
		try:
			if(stock_entry):
				doc = frappe.get_doc("Stock Entry", stock_entry.parent)
				if (doc.docstatus == 1):
					doc.cancel()
		except Exception as e:
			frappe.throw(f"An error occurred while canceling the document: {e}")

def get_item_group(item_group_name):
	if(item_group_name):
		if(frappe.db.exists("Item Group", item_group_name)):
			return item_group_name
		
		doc = frappe.new_doc("Item Group")
		doc.item_group_name = item_group_name
		doc.insert(ignore_permissions=True)
		return doc.name

def get_brand(brand):
	if(frappe.db.exists("Brand", brand)):
		return brand
	doc = frappe.get_doc("Brand",{
			"brand": brand
		})
	doc.insert(ignore_permissions=True)
	return doc.name

# bench --site zirconprod.3xg.africa execute ecommerce.ecommerce.doctype.products.products.updateP
def updateP():
	for d in frappe.db.sql('''select * from `tabProducts` where ifnull(item_code, '')!=''  ''', as_dict=1):
		frappe.db.sql(f'''update `tabProducts` set name='{d.item_code}' where name='{d.name}' ''')