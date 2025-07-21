import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

### Function to List All Orders for a User
def list_orders(user_id):
	try:
		orders = frappe.get_all(
			"Order",
			filters={"user_id": user_id},
			fields=[
				"name", 
				"order_id",
				"email",
				"user_id",
				"net_total",
				"discount",
				"shipping_fee",
				"grand_total",
				"payment_method",
				"status",
				"coupon_code"
			]
		)
		
		if not orders:
			return create_response(NOT_FOUND, [])

		all_orders = []

		for order in orders:
			created_order = frappe.get_doc("Order", order["name"])
			
			order_data = created_order.as_dict()

			for item in created_order.items:
				order_data["items"].append({
					"item_code": item.item_code,
					"price": item.price,
					"quantity": item.quantity,
					"image": item.image,
					"seller_id": item.seller_id,
					"seller_name": item.seller_name,
					"seller_location_lat": item.seller_location_lat,
					"seller_location_long": item.seller_location_long,
				})

			all_orders.append(order_data)

		return create_response(SUCCESS, all_orders)

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching orders and cart items")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def list_orders_by_merchant(merchant_id):
	try:
		orders = frappe.get_all(
			"Order",
			filters={},
			fields=[
				"name",
				"order_id",
				"email",
				"user_id",
				"net_total",
				"discount",
				"shipping_fee",
				"grand_total",
				"payment_method",
				"status",
				"coupon_code"
			]
		)

		all_orders = []

		for order in orders:
			created_order = frappe.get_doc("Order", order["name"])

			items_for_merchant = [
				{
					"item_code": item.item_code,
					"price": item.price,
					"quantity": item.quantity,
					"seller_id": item.seller_id,
					"seller_name": item.seller_name,
					"seller_location_lat": item.seller_location_lat,
					"seller_location_long": item.seller_location_long,
				}
				for item in created_order.items if item.seller_id == merchant_id
			]

			if not items_for_merchant:
				continue

			order_data = {
				"order_id": created_order.order_id,
				"email": created_order.email,
				"user_id": created_order.user_id,
				"subtotal": created_order.net_total,
				"discount": created_order.discount,
				"shipping_fee": created_order.shipping_fee,
				"grand_total": created_order.grand_total,
				"payment_method": created_order.payment_method,
				"status": created_order.status,
				"items": items_for_merchant,
			}

			all_orders.append(order_data)

		if not all_orders:
			return create_response(SUCCESS, {
				"message": f"No orders found for merchant_id: {merchant_id}.",
				"data": []
			})

		return create_response(SUCCESS, all_orders)

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching orders by merchant ID")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def get_single_order(user_id, order_id):
	try:
		order_query = """
			SELECT *
			FROM `tabOrder`
			WHERE user_id = %s AND order_id = %s
		"""
		order = frappe.db.sql(order_query, (user_id, order_id), as_dict=True)

		if not order:
			return create_response(NOT_FOUND, [])

		order = order[0]

		order_items_query = """
			SELECT *
			FROM `tabOrder Item`
			WHERE parent = %s
		"""
		order_items = frappe.db.sql(order_items_query, (order["name"],), as_dict=True)

		order["items"] = order_items

		return create_response(SUCCESS, {
			"message": "Order retrieved successfully.",
			"data": order
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, {"message": f"Order not found: {str(e)}"})
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching single order")
		return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})

def creating_order(args: dict):
	try:
		args = frappe._dict(args)
		merchant_cache = {}
		validated_items = []
		
		def validate_user():
			if not frappe.db.exists("Website User", {"name": args.email}):
				raise ValueError(f"Customer is not found on ERP with <b>{args.email}</b>")
		
		validate_user()

		for row in args.get("items", []):  # Ensure items is a list
			row = frappe._dict(row)
			product_details = frappe.db.get_value(
				"Products",
				{"name": row.item_code},
				"*",
				as_dict=True
			)
			
			if not product_details:
				raise ValueError(create_response(NOT_FOUND, {"message": f"Item not found: {row.item_code}"}))

			merchant_id = product_details["merchant_id"]
			if merchant_id not in merchant_cache:
				merchant_details = frappe.db.get_value(
					"Merchants",
					{"merchant_id": merchant_id},
					["merchant_id", "business_name", "business_location", "phone", "business_location_lat", "business_location_long"],
					as_dict=True
				)

				if not merchant_details:
					raise ValueError(create_response(NOT_FOUND, {"message": f"Merchant not found for item: {row.item_code}"}))

				merchant_cache[merchant_id] = merchant_details
			else:
				merchant_details = merchant_cache[merchant_id]

			validated_items.append({
				"doctype": "Order Item",
				"user_id": args.user_id,
				"item_code": row.item_code,
				"product_name": row.get("product_name"),
				"price": row.get("price"),
				"quantity": row.get("quantity"),
				"image": row.get("business_name"),
				"seller_name": row.get("image"),
			})

		if merchant_cache:
			sales_order = frappe.get_doc({
				"doctype": "Order",
				"shipping_address": args.shipping_address,
				"lga": args.lga,
				"post_code": args.post_code,
				"net_total": args.subtotal,
				"discount": args.discount,
				"shipping_fee": args.shipping_fee,
				"grand_total": args.grand_total,
				"payment_method": args.payment_method,
				"order_id": args.order_id,
				"user_id": args.user_id,
				"email": args.email,
				"status": "Ongoing",
				"items": validated_items,
				"coupon_code": args.coupon_code,
				"platform": args.platform,
				"escrow_release_date": args.escrow_release_date,
				"is_paid": 1
			})
			
			sales_order.insert(ignore_permissions=True)
			frappe.db.commit()
			return create_response(SUCCESS, {"order_id": sales_order.name})

	except ValueError as e:
		frappe.log_error(f"Data validation error for user {args.user_id}: {str(e)}", "Order Creation Validation Error")
		return create_response(BAD_REQUEST, {"message": f"Validation error: {str(e)}"})
	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error for user {args.user_id}: {str(e)}", "Order Creation Validation Error")
		return create_response(BAD_REQUEST, {"message": f"Frappe validation error: {str(e)}"})
	except Exception as e:
		frappe.log_error(f"Error creating order for user {args.user_id}: {str(e)}", "Order Creation Error")
		return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})

def update_order(order_id, user_id, is_paid=None, subtotal=None, shipping_address=None, post_code=None, lga=None, discount=None, shipping_fee=None, grand_total=None, payment_method=None, status=None, items=None):
	pass

def updating_order(args: dict):
	try:
		args = frappe._dict(args)
		sales_order = frappe.get_doc("Order", args.order_id)
		
		if not sales_order:
			raise ValueError(f"Order with ID {args.order_id} does not exist.")

		if args.user_id and sales_order.user_id != args.user_id:
			raise ValueError("User ID does not match the owner of the order.")
		
		if args.is_paid is not None:
			sales_order.is_paid = args.is_paid

		if args.subtotal is not None:
			sales_order.net_total = args.subtotal
		if args.shipping_address is not None:
			sales_order.shipping_address = args.shipping_address
		if args.post_code is not None:
			sales_order.post_code = args.post_code
		if args.lga is not None:
			sales_order.lga = args.lga
		if args.discount is not None:
			sales_order.discount = args.discount
		if args.shipping_fee is not None:
			sales_order.shipping_fee = args.shipping_fee
		if args.grand_total is not None:
			sales_order.grand_total = args.grand_total
		if args.payment_method is not None:
			sales_order.payment_method = args.payment_method
		if args.status is not None:
			sales_order.status = args.status

		if (not args.get("items")):
			required_keys = ["item_code", "price", "quantity", "seller_name"]
			
			if not isinstance(args.get("items"), list) or not all(isinstance(item, dict) for item in args.get("items")):
				raise ValueError("Items must be a list of dictionaries.")
			
			validated_items = []
			for item in args.get("items"):
				if not all(key in item for key in required_keys):
					raise ValueError("Each item must include item_code, price, quantity, and seller_name.")
				validated_items.append({
					"item_code": item["item_code"],
					"price": item["price"],
					"quantity": item["quantity"],
					"seller_name": item["seller_name"],
					"user_id": item.get("user_id", sales_order.user_id),
				})
			
			sales_order.items = validated_items

		sales_order.save()
		frappe.db.commit()

		return create_response(SUCCESS, {"order_id": sales_order.name, "message": "Order updated successfully."})

	except ValueError as e:
		frappe.log_error(f"Data validation error for user {args.user_id}: {str(e)}", "Order Update Validation Error")
		return create_response(BAD_REQUEST, f"Validation error: {str(e)}")

	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error for user {args.user_id}: {str(e)}", "Order Update Validation Error")
		return create_response(BAD_REQUEST, f"{str(e)}")

	except Exception as e:
		frappe.log_error(f"Error updating order for user {args.user_id}: {str(e)}", "Order Update Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


def update_order_status(order_id: str, new_status: str):
	try:
		order = frappe.get_doc("Order", {'order_id': order_id})
		if not order:
			return create_response(NOT_FOUND, {"message": f"Order {order_id} not found"})

		order.status = new_status
		order.save(ignore_permissions=True)
		frappe.db.commit()

		return create_response(SUCCESS, {"message": f"Order {order_id} status updated to {new_status}"})

	except frappe.DoesNotExistError:
		return create_response(NOT_FOUND, {"message": f"Order {order_id} not found"})
	except Exception as e:
		frappe.log_error(f"Error updating order {order_id}: {str(e)}", "Order Update Error")
		return create_response(SERVER_ERROR, {"message": f"An error occurred: {str(e)}"})


def update_payment(user_id, order_id):
	try:
		query = """
			SELECT is_paid
			FROM `tabOrder`
			WHERE order_id = %s AND user_id = %s
		"""
		order = frappe.db.sql(query, (order_id, user_id), as_dict=True)

		if not order:
			return create_response(NOT_FOUND, f"Order with order_id {order_id} not found for user_id {user_id}.")

		current_status = order[0].get("is_paid", 0)
		new_status = 0 if current_status == 1 else 1
		status_message = "paid" if new_status == 1 else "unpaid"

		update_query = """
			UPDATE `tabOrder`
			SET is_paid = %s
			WHERE order_id = %s AND user_id = %s
		"""
		frappe.db.sql(update_query, (new_status, order_id, user_id))
		frappe.db.commit()

		return create_response(SUCCESS, {
			"message": f"Order with order_id {order_id} is now {status_message}.",
			"data": {"order_id": order_id, "user_id": user_id, "is_paid": new_status}
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, f"Error: {str(e)}")

	except Exception as e:
		frappe.log_error(message=str(e), title="Error toggling order payment status")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def delete_order(user_id, order_id):
	try:
		if order_id:
			if not frappe.db.exists("Order", {"user_id": user_id, "name": order_id}):
				return create_response(SUCCESS, f"{order_id} not found in order for user {user_id}.")
		else:
			if not frappe.db.exists("Order", {"user_id": user_id}):
				return create_response(SUCCESS, f"Order not found for user {user_id}.")

		if order_id:
			frappe.db.sql("""
				DELETE FROM `tabOrder`
				WHERE user_id = %s AND name = %s
			""", (user_id, order_id))
			
			message = f"{order_id} order has been deleted successfully."
		else:
			frappe.db.sql("""
				DELETE FROM `tabOrder`
				WHERE user_id = %s
			""", (user_id))
			message = f"Order for user {user_id} deleted successfully!"

		frappe.db.commit()
		return create_response(SUCCESS, message)

	except frappe.DoesNotExistError as e:
		frappe.log_error(f"Order does not exist: {str(e)}", "Delete Order Error")
		return create_response(SUCCESS, "Order item or order does not exist.")
	except Exception as e:
		frappe.log_error(f"Error deleting order or item for user {user_id}: {str(e)}", "Delete Order Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def order_return_request(args: dict):
	try:
		args = frappe._dict(args)

		if(frappe.db.exists("Order Return Request", args.id)):
			return create_response(SUCCESS, 
				{"data": {"id": args.id}, "message": "Order return request is already exist."}
			)
		cargs = {
			"doctype": "Order Return Request",
			"id": args.id,
			"orderitemid": args.orderItemId,
			"reason": args.reason,
			"quantity": args.quantity,
			"media": args.media,
			"lat": args.address.get("lat"),
			"long": args.address.get("long"),
			"address": args.address.get("address"),
			"receipt": args.receipt,
			"comment": args.comment
		} 
		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return create_response(SUCCESS, {"data": doc, "message": "Order return request submitted successfully."})

	except frappe.DoesNotExistError as e:
		frappe.log_error(f"Order does not exist: {str(e)}", "Order return request error")
		return create_response(SUCCESS, "Order item or order does not exist.")
	except Exception as e:
		frappe.log_error(f"Error posting order return request", "Order return request error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


