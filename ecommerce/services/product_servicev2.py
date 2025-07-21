import frappe
import json
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

### Get all items
def list_items(filters=None):
	try:
		query = """
			SELECT name, item_code, sku, product_name, actual_price, discounted_price, image, rating, color, category, sub_category, sub_sub_category, brand, discount, quantity, warranty_period, is_favourite
			FROM `tabProducts`
			WHERE 1=1
		"""
		params = []

		if filters:
			if filters.get("product_name"):
				query += " AND product_name LIKE %s"
				params.append(f"%{filters['product_name']}%")

			if filters.get("min_price") is not None:
				query += " AND discounted_price >= %s"
				params.append(filters["min_price"])

			if filters.get("max_price") is not None:
				query += " AND discounted_price <= %s"
				params.append(filters["max_price"])

			if filters.get("color"):
				query += " AND color = %s"
				params.append(filters["color"])

			if filters.get("category"):
				query += " AND category = %s"
				params.append(filters["category"])
				
			if filters.get("sub_category"):
				query += " AND sub_category = %s"
				params.append(filters["sub_category"])
				
			if filters.get("sub_sub_category"):
				query += " AND sub_sub_category = %s"
				params.append(filters["sub_sub_category"])

			if filters.get("brand"):
				query += " AND brand = %s"
				params.append(filters["brand"])

			if filters.get("rating"):
				query += " AND rating >= %s"
				params.append(filters["rating"])

			if filters.get("discount"):
				query += " AND discount >= %s"
				params.append(filters["discount"])
				
			if filters.get("collection"):
				query += " AND collection >= %s"
				params.append(filters["collection"])

		products = frappe.db.sql(query, params, as_dict=True)

		if not products:
			return create_response(NOT_FOUND, [])

		all_items = []
		for product in products:
			specifications = frappe.get_all(
				"Specifications",
				filters={"parent": product["name"]},
			)

			product_data = {
				"item_code": product["item_code"],
				"sku": product["sku"],
				"product_name": product["product_name"],
				"actual_price": product["actual_price"],
				"discounted_price": product["discounted_price"],
				"image": product["image"],
				"rating": product["rating"],
				"color": product["color"],
				"category": product["category"],
				"sub_category": product["sub_category"],
				"sub_sub_category": product["sub_sub_category"],
				"brand": product["brand"],
				"discount": product["discount"],
				"quantity": product["quantity"],
				"warranty_period": product["warranty_period"],
				"is_favourite": product["is_favourite"],
				"specifications": specifications
			}
			all_items.append(product_data)

		return create_response(SUCCESS, all_items)

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching items and specifications")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def get_single_product(item_code):
	try:
		query = """
			SELECT *
			FROM `tabProducts`
			WHERE item_code = %s
		"""

		product = frappe.db.sql(query, (item_code,), as_dict=True)
		
		if not product:
			return create_response(SUCCESS, f"Product with item_code {item_code} not found.")

		return create_response(SUCCESS, product)

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))

	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching product")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def get_all_products_by_merchant_id(merchant_id):
	try:
		query = """
			SELECT *
			FROM `tabProducts`
			WHERE merchant_id = %s
		"""
		
		product = frappe.db.sql(query, (merchant_id,), as_dict=True)

		if not product:
			return create_response(NOT_FOUND, [])

		return create_response(SUCCESS, {
			"message": "Product fetched successfully.",
			"data": product 
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching merchant by ID")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

# Get product by merchant ID
def get_product_by_merchant_id(item_code, merchant_id):
	try:
		query = """
			SELECT *
			FROM `tabProducts`
			WHERE item_code = %s AND merchant_id = %s
		"""
		
		product = frappe.db.sql(query, (item_code, merchant_id), as_dict=True)

		if not product:
			return create_response(NOT_FOUND, [])

		return create_response(SUCCESS, {
			"message": "Product fetched successfully.",
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching product by merchant ID and item code")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def get_product_by_brands(brand):
	try:
		query = """
			SELECT *
			FROM `tabProducts`
			WHERE brand = %s
		"""
		brands = frappe.db.sql(query, (brand,), as_dict=True)

		if not brands:
			return create_response(NOT_FOUND, {
				"message": f"No products found for the brand '{brand}'.",
				"data": []
			})

		return create_response(SUCCESS, {
			"message": f"Products for the brand '{brand}' retrieved successfully.",
			"data": brands
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, {
			"message": "Brand does not exist.",
			"data": []
		})
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching products by brand")
		return create_response(SERVER_ERROR, {
			"message": f"An unexpected error occurred: {str(e)}"
		})

def list_similar_products(item_code):
	try:
		if (not frappe.db.exists("Products", {"item_code": item_code})):
			raise ValueError(f"Item with code '{item_code}' not exists!")
		
		""" fetch similar products based on 
		{category, brand, discounted_price, discounted_price}
		"""
		product_detail = frappe.db.sql(""" 
			Select category, brand, discounted_price
			From `tabProducts`
			Where item_code = %(item_code)s """,
			{
				"item_code": item_code
			}, as_dict=1)
		# return product_detail
		for row in product_detail:
			similar_products = frappe.db.sql("""
				SELECT *
				FROM `tabProducts`
				WHERE 
					item_code != %(item_code)s
					and (category = %(category)s or
					brand = %(brand)s or
					discounted_price BETWEEN %(min_price)s AND %(max_price)s)
				ORDER BY 
					rating DESC
				LIMIT 10
			""", {
				"item_code": item_code,
				"category": row.category,
				"brand": row.brand,
				"min_price": row.discounted_price * 0.8,
				"max_price": row.discounted_price * 1.2
			}, as_dict=True)
		
			return create_response(SUCCESS, similar_products)
	
	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching similar products")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def list_items_category(limit=8, offset=0, search=None, letter=None, category=None, min_price=None, max_price=None):
	try:
		query = """
			SELECT item_code, product_name, category, actual_price, discounted_price, image, rating, brand, description, collection, model, weight, color, quantity, warranty, is_favourite
			FROM `tabProducts`
			WHERE 1=1
		"""
		
		filters = []
		
		if search:
			query += " AND (product_name LIKE %s OR description LIKE %s)"
			filters.extend([f"%{search}%", f"%{search}%"])

		if letter:
			query += " AND (product_name LIKE %s OR description LIKE %s)"
			filters.extend([f"{letter}%", f"{letter}%"])

		if category:
			query += " AND category = %s"
			filters.append(category)

		if min_price is not None:
			query += " AND discounted_price >= %s"
			filters.append(min_price)
		
		if max_price is not None:
			query += " AND discounted_price <= %s"
			filters.append(max_price)

		query += " LIMIT %s OFFSET %s"
		filters.extend([limit, offset])
		
		items = frappe.db.sql(query, filters, as_dict=True)

		if not items:
			return create_response(NOT_FOUND, [])

		categories = {}
		collections = {}
		stores = {}

		for item in items:
			category_name = item['category']
			if category_name not in categories:
				categories[category_name] = {
					'category': category_name,
					'products': []
				}
			categories[category_name]['products'].append(item)

			collection_name = item['collection']
			if collection_name not in collections:
				collections[collection_name] = {
					'collection': collection_name,
					'products': []
				}
			collections[collection_name]['products'].append(item)

		categories_list = list(categories.values())
		collections_list = list(collections.values())

		return create_response(SUCCESS, {
			'Categories': categories_list,
			'Collections': collections_list,
			'Stores': stores 
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching items")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


### Get single item by code
def get_item_by_code(item_code):
	try:
		item = frappe.get_doc("Products", {"item_code": item_code})

		if not item:
			raise frappe.DoesNotExistError(f"Item with code {item_code} not found!")

		return create_response(SUCCESS, item.as_dict())

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching single item")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



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

def add_new_item(
	item_code,
	product_name=None,
	category=None,
	sub_category=None,
	sub_sub_category=None,
	actual_price=None,
	discounted_price=None,
	discount=None,
	image=None,
	images=None,
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
	merchant_id=None,
	status=None,
	createdAt=None
):
	try:
		actual_price = float(actual_price) if actual_price else None
		discounted_price = float(discounted_price) if discounted_price else None
		discount = float(discount) if discount else None
		rating = float(rating) if rating else None
		quantity = int(quantity) if quantity else None
		weight = str(weight) if weight else None

		validate_item_data(actual_price, discounted_price, discount, rating, quantity, weight)

		if frappe.db.exists("Products", {"merchant_id": merchant_id, "item_code": item_code}):
			# raise ValueError(f"Item with code '{item_code}' already exists!")
			raise ValueError("Item already exists!")

		
		spec_obj = []
		if specifications:
			try:
				specs = specifications  if(isinstance(specifications, (list, dict))) else json.loads(specifications)
				for row in specs:
					spec_obj.append(row)
					# for key, value in row.items():
					# spec_obj.append({"key": key, "value": value})
			except json.JSONDecodeError:
				frappe.throw("Invalid format for specifications. Must be a valid JSON string.")

		color_obj = []
		if color:
			try:
				colors = color if(isinstance(color, (list, dict))) else json.loads(color)
				color_obj = [{"color": col.get("color")} for col in colors]
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
			"images": frappe.as_json(images),
			# "images": str(images),
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
			"status": status,
			"created_at": createdAt,
		})
		new_item.insert(ignore_permissions=True)
		frappe.db.commit()
		rbody = {
			"item_code": new_item.item_code,
			"sku": new_item.sku,
			"message": f"Item added successfully!"
		}
		return create_response(SUCCESS, rbody)

	except ValueError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(f"Error adding new item: {str(e)}", "Add Item Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Update existing item
def updating_item(args: dict):
	args = frappe._dict(args)
	
	def arrange_specifications():
		spec_obj = []
		if args.specifications:
			for row in args.specifications:
				for key, value in row.items():
					spec_obj.append({"key": key, "value": value})
		return spec_obj
	
	def arrange_colors():
		if args.color:
			return [{"color": col} for col in (args.color)]            
	
	try:
		if (not frappe.db.exists("Products", {
    		"merchant_id": args.merchant_id, 
			"item_code": args.item_code
   		})):
			return create_response(NOT_FOUND, {
				"message": f"Item code '{args.item_code}' not found.",
				"data": []
			})
		else:
			doc = frappe.get_doc("Products", {"item_code": args.item_code})
			doc.merchant_id= args.merchant_id
			doc.created_at= args.createdAt
			doc.product_name= args.product_name
			doc.status= "IN_REVIEW"
			doc.category= args.category
			doc.sub_category= args.sub_category
			doc.sub_sub_category= args.sub_sub_category
			doc.actual_price= args.actual_price
			doc.discounted_price= args.discounted_price
			doc.discount= args.discount
			doc.images= frappe.as_json(args.images)
			doc.rating= args.rating
			doc.description= args.description
			doc.set("specifications", arrange_specifications())
			doc.set("color", arrange_colors())
			doc.quantity= args.quantity
			doc.collection= args.collection
			doc.weight= args.weight
			doc.warranty= args.warranty

			doc.brand = args.brand
			doc.model = args.model
			doc.status = args.status

			doc.save(ignore_permissions=True)
			frappe.db.commit()
			return create_response(SUCCESS, {
				"message": f"Item updated successfully!",
				"data": doc
			})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(f"Error updating item with code '{args.item_code}': {str(e)}", "Update Product Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

### Delete item by code
def delete_product(item_code, merchant_id):
	try:
		product = frappe.db.exists("Products", {"item_code": item_code, "merchant_id": merchant_id})
		if not product:
			return create_response(SUCCESS, {
				"message": f"Item with code '{item_code}' not found for the given merchant.",
				"data": []
			})

		frappe.db.sql("""
			DELETE FROM `tabProducts`
			WHERE item_code = %s AND merchant_id = %s
		""", (item_code, merchant_id))
		frappe.db.commit()

		return create_response(SUCCESS, f"Item '{item_code}' deleted successfully!")

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(f"Error deleting item '{item_code}': {str(e)}", "Delete Product Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def reduce_product_quantity(item_code, quantity_to_reduce):
	try:
		product = frappe.get_doc("Products", {"item_code": item_code})

		if not product:
			return create_response(SUCCESS, {
				"message": f"Product with item_code '{item_code}' not found.",
				"data": []
			})

		if quantity_to_reduce <= 0:
			return create_response(BAD_REQUEST, {
				"message": "Quantity to reduce must be greater than 0.",
			})

		if product.quantity < quantity_to_reduce:
			return create_response(BAD_REQUEST, {
				"message": f"Insufficient stock. Available quantity: {product.quantity}",
			})

		product.quantity -= quantity_to_reduce
		product.save()

		return create_response(SUCCESS, {
			"message": f"Product quantity reduced successfully. Remaining quantity: {product.quantity}",
			"data": {
				"item_code": product.item_code,
				"remaining_quantity": product.quantity
			}
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error reducing product quantity")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def toggle_product_visibility(item_code, merchant_id):
	try:
		query = """
			SELECT is_disabled
			FROM `tabProducts`
			WHERE item_code = %s AND merchant_id = %s
		"""
		product = frappe.db.sql(query, (item_code, merchant_id), as_dict=True)

		if not product:
			return create_response(SUCCESS, f"Product with item_code {item_code} not found or does not belong to the merchant.")

		current_status = product[0].get("is_disabled", 0)
		new_status = 0 if current_status == 1 else 1

		update_query = """
			UPDATE `tabProducts`
			SET is_disabled = %s
			WHERE item_code = %s AND merchant_id = %s
		"""
		frappe.db.sql(update_query, (new_status, item_code, merchant_id))
		frappe.db.commit()

		status_message = "disabled" if new_status == 1 else "enabled"
		return create_response(SUCCESS, {
			"message": f"Product with item_code {item_code} has been {status_message} successfully.",
			"data": {"item_code": item_code, "is_disabled": new_status}
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))

	except Exception as e:
		frappe.log_error(message=str(e), title="Error toggling product visibility")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def hide_show(item_code, merchant_id):
	try:
		query = """
			SELECT is_hidden
			FROM `tabProducts`
			WHERE item_code = %s AND merchant_id = %s
		"""
		product = frappe.db.sql(query, (item_code, merchant_id), as_dict=True)
		
		if not product:
			return create_response(SUCCESS, f"Product with item_code {item_code} not found or does not belong to the merchant.")

		current_status = product[0].get("is_hidden", 0)
		new_status = 0 if current_status == 1 else 1

		update_query = """
			UPDATE `tabProducts`
			SET is_hidden = %s
			WHERE item_code = %s AND merchant_id = %s
		"""
		frappe.db.sql(update_query, (new_status, item_code, merchant_id))
		frappe.db.commit()

		status_message = "hidden" if new_status == 1 else "visible"
		return create_response(SUCCESS, {
			"message": f"Product with item_code {item_code} is now {status_message}.",
			"data": {"item_code": item_code, "is_hidden": new_status}
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))

	except Exception as e:
		frappe.log_error(message=str(e), title="Error toggling product visibility")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def list_sorted_products(popularity, time_created, price):
	def get_product_by_popularity():
		data = frappe.db.sql(""" 
				select od.name, 
				itm.item_code, 
				itm.product_name,
				p.name as product_id, 
				p.image, 
				p.rating, 
				p.category,
				p.brand, 
				p.actual_price, 
				p.discounted_price, 
				p.discount,
				sum(itm.quantity) as qty
			From 
				`tabOrder` od inner join `tabOrder Item` itm on (od.name=itm.parent) inner join `tabProducts` p on (itm.item_code=p.item_code)
			Where 
				od.docstatus=0
			Group by 
				itm.item_code
			Order by 
				qty desc """, as_dict=1)
		for d in data:
			d.update({"color": [c.color for c in frappe.db.sql(f""" Select color from `tabProduct Color` where parent='{d.product_id}' """, as_dict=1)]})
		return data
	
	def get_product_time_created():
		data = frappe.db.sql(""" 
			Select 
				name, 
				item_code, 
				product_name, 
				image, 
				rating,
				category,
				brand, 
				actual_price, 
				discounted_price, 
				discount
			From 
				`tabProducts`
			Where 
				docstatus=0
			Order by 
				creation desc """, as_dict=1)
		for d in data:
			d.update({"color": [c.color for c in frappe.db.sql(f""" Select color from `tabProduct Color` where parent='{d.name}' """, as_dict=1)]})    
		return data
	
	def get_product_price():
		data = frappe.db.sql(""" 
		Select 
			name, 
			item_code, 
			product_name, 
			image, 
			rating,
			category,
			brand, 
			actual_price, 
			discounted_price, 
			discount
		From 
			`tabProducts`
		Where 
			docstatus=0
		Order by 
			actual_price desc """, as_dict=1)
		for d in data:
			d.update({"color": [c.color for c in frappe.db.sql(f""" Select color from `tabProduct Color` where parent='{d.name}' """, as_dict=1)]})    
		return data
	
	if(popularity):
		return get_product_by_popularity()
	elif(time_created):
		return get_product_time_created()
	elif(price):
		return get_product_price()
	return list_items()
