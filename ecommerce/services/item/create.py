import frappe
import json
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

# bench --site zirconprod.3xg.africa execute ecommerce.services.item.create.add_item
@frappe.whitelist(allow_guest=True)
def add_item():
    # frappe.log_error(message=f"Incoming kwargs: {kwargs}", title="Debug - Add Item")
	args = {
		"actual_price": 10,
		"discounted_price": 8,
		"discount": 2.0

	}
	allowed_keys = [
		"product_name", "category", "sub_category", "sub_sub_category",
		"actual_price", "discounted_price", "discount", "image", "rating",
		"brand", "description", "specifications", "collection", "model",
		"weight", "color", "quantity", "warranty", "merchant_id"
	]

	filtered_kwargs = {key: value for key, value in args.items() if key in allowed_keys}

	return add_new_item(**filtered_kwargs)

def add_new_item(
	product_name=None,
	category=None,
	sub_category=None,
	sub_sub_category=None,
	actual_price=None,
	discounted_price=None,
	discount=None,
	image=None,
	rating=None,
	brand=None,
	description=None,
	specifications=None,
	collection=None,
	model=None,
	weight=None,
	color=None,
	quantity=None,
	warranty=None,
	merchant_id=None
):
	actual_price = float(actual_price) if actual_price else None
	# discounted_price = float(discounted_price) if discounted_price else None
	# discount = float(discount) if discount else None
	# rating = float(rating) if rating else None
	# quantity = int(quantity) if quantity else None
	# weight = str(weight) if weight else None
	print(f"{actual_price} {discounted_price} {discount}")
	""" try:
		actual_price = float(actual_price) if actual_price else None
		discounted_price = float(discounted_price) if discounted_price else None
		discount = float(discount) if discount else None
		rating = float(rating) if rating else None
		quantity = int(quantity) if quantity else None
		weight = str(weight) if weight else None

		validate_item_data(actual_price, discounted_price, discount, rating, quantity, weight)

		if frappe.db.exists("Products", {"item_code": item_code}):
			raise ValueError(f"Item with code '{item_code}' already exists!")

		
		spec_obj = []
		if specifications:
			try:
				specs = json.loads(specifications)
				for row in specs:
					for key, value in row.items():
						spec_obj.append({"key": key, "value": value})
			except json.JSONDecodeError:
				frappe.throw("Invalid format for specifications. Must be a valid JSON string.")

		color_obj = []
		if color:
			try:
				colors = json.loads(color)
				color_obj = [{"color": col} for col in colors]
			except json.JSONDecodeError:
				frappe.throw("Invalid format for color. Must be a valid JSON string.")

		new_item = frappe.get_doc({
			"doctype": "Products",
			"item_code": item_code,
			"product_name": product_name,
			"category": category,
			"sub_category": sub_category,
			"sub_sub_category": sub_sub_category,
			"actual_price": actual_price,
			"discounted_price": discounted_price,
			"discount": discount,
			"image": image,
			"rating": rating,
			"brand": brand,
			"description": description,
			"specifications": spec_obj,
			"color": color_obj,
			"quantity": quantity,
			"collection": collection,
			"model": model,
			"weight": weight,
			"warranty": warranty,
			"merchant_id": merchant_id,
		})
		new_item.insert(ignore_permissions=True)
		frappe.db.commit()

		return create_response(SUCCESS, f"Item '{item_code}' added successfully!")

	except ValueError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(f"Error adding new item: {str(e)}", "Add Item Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")"""

def validate_item_data(actual_price, discounted_price, discount, rating, quantity, weight):
	"""Validates numeric fields to ensure they are of the correct type."""
	if actual_price is not None and not isinstance(actual_price, (int, float)):
		frappe.throw("Actual price must be a number.")
	if discounted_price is not None and not isinstance(discounted_price, (int, float)):
		frappe.throw("Discounted price must be a number.")
	if discount is not None and not isinstance(discount, (int, float)):
		frappe.throw("Discount must be a number.")
	if rating is not None and not isinstance(rating, (int, float)):
		frappe.throw("Rating must be a number.")
	if quantity is not None and not isinstance(quantity, int):
		frappe.throw("Quantity must be an integer.")
	if weight is not None and not isinstance(weight, str):
		frappe.throw("Weight must be an string.")

