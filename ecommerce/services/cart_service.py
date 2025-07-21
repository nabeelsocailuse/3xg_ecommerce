import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

def create_update_cart(args: dict):
	try:
		args = frappe._dict(args)
		
		web_user = frappe.db.get_value("Website User", {"user_id": args.userId, "email": args.email}, "name")
		
		if (not web_user):
			return create_response(NOT_FOUND, f"User with {args.userId}: {args.email} not found.")

		cart = frappe.db.get_value("Cart", {"userid": args.userId, "email": args.email}, "name")

	   
		itemsList = [{
				"productid": row["productId"],
				# "productname": row.productName,
				"quantity": row["quantity"],
				"price": row["price"],
				"discountedprice": row["discountedPrice"]
			} for row in args["items"]
			]
		cargs = {
				"items": itemsList,
				"totalprice": args.totalPrice,
				"itemsprice": args.itemsPrice,
				"shippingprice": args.shippingPrice,
				"totaldiscount": args.totalDiscount,
				"coupondiscount": args.couponDiscount,
				"totalprice": args.totalPrice,
				"couponapplied": args.couponApplied,
				"couponcode":  args.couponCode,
			}
		
		if cart:
			doc = frappe.get_doc("Cart", cart)
			doc.update(cargs)
			doc.save(ignore_permissions=True)
		else:
			cargs.update({
				"doctype": "Cart",
				"userid": args.userId,
				"email": args.email
			})
			frappe.get_doc(cargs).insert(ignore_permissions=True)

		frappe.db.commit()
		return create_response(SUCCESS, "Cart updated successfully!" if(cart) else "Cart added successfully!")

	except frappe.DuplicateEntryError:
		return create_response(SERVER_ERROR, "Duplicate entry found. Please try again.")
	except Exception as e:
		frappe.log_error(f"Error adding items to cart for user {args.email}: {str(e)}", "Add to Cart Error")
		return create_response(SERVER_ERROR, f"An unexpected error occurred while adding the item: {str(e)}")

def read_cart_list(userId):
	try:
		# args = frappe._dict(args)
		cart = frappe.db.sql(f"""
				SELECT *
				FROM `tabCart`
				WHERE userid = '{userId}'
			""", as_dict=True)
		cartDict = {}
		if(cart):
			for obj in cart:
				cartItems = frappe.db.sql(f"""
						SELECT *
						FROM `tabCart Item`
						WHERE parent = '{obj.name}'
					""", as_dict=True)

				cartDict.update({
					"userId": obj.userid,
					"email": obj.email,
					"items": [
						{       
						"productId": row.productid,
						"productName": row.productname,
						"quantity": row.quantity,
						"price": row.price,
						"discountedPrice": row.discountedprice
						}
					for row in cartItems],
					"itemsPrice": obj.itemsprice,
					"shippingPrice": obj.shippingprice,
					"totalDiscount": obj.totaldiscount,
					"couponDiscount": obj.coupondiscount,
					"totalPrice": obj.totalprice,
					"couponApplied": obj.couponapplied,
					"couponCode":  obj.couponcode,
				})
		if not cartDict:
			return create_response(NOT_FOUND, [])

		return create_response(SUCCESS, cartDict)

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error fetching items")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def update_cart_quantity(user_id, item_code, quantity):
	try:
		query_check = """
			SELECT *
			FROM `tabCart`
			WHERE user_id = %s AND item_code = %s
		"""
		item = frappe.db.sql(query_check, (user_id, item_code), as_dict=True)

		if not item:
			return create_response(NOT_FOUND, [])

		query_update = """
			UPDATE `tabCart`
			SET quantity = %s
			WHERE user_id = %s AND item_code = %s
		"""
		frappe.db.sql(query_update, (quantity, user_id, item_code))
		frappe.db.commit()

		return create_response(SUCCESS, "Quantity updated successfully.")

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error updating cart quantity")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def delete_cart(userId):
	try:
		if(not frappe.db.exists('Cart', {'userid': userId})):
			return create_response(NOT_FOUND, {
				"message": "No cart found."
			}) 

		doc = frappe.get_doc('Cart', {'userid': userId})
		doc.delete(ignore_permissions=True)
		return create_response(SUCCESS, {
			"message": "Cart cleared successfully."
		})

	except frappe.DoesNotExistError as e:
		return create_response(SUCCESS, str(e))
	except Exception as e:
		frappe.log_error(message=str(e), title="Error clearing cart")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
