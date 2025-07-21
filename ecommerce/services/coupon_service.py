import frappe
from ecommerce.utils.response_helper import create_response
from ecommerce.constants.http_status import (
	SUCCESS, 
	NOT_FOUND, 
	SERVER_ERROR, 
	BAD_REQUEST
)

def get_coupons_list(args: dict):
	try:
		args = frappe._dict(args)
		data =  frappe.db.sql(f"""
			Select 
				coupon_type,
				coupon_name,
				coupon_code,
				group,
				description,
				maximum_use,
				used,
				valid_from,
				valid_upto,
				pricing_rule,
				apply_on,
				rate_or_discount,
				discount_percentage,
				discount_amount
			From 
				`tabCoupon Code`
			Where 
				docstatus=0
				{"and apply_on_platform = %(apply_on_platform)s" if(args.get("apply_on_platform")) else ""}
			""", args , as_dict=1)
		
		for row in data:
			row["pricing_rule"] = {
				"id": row.pricing_rule,
				"items": get_items(row.pricing_rule)
			}
		return create_response(SUCCESS, {"data": data})
	
	except ValueError as e:
		# for user {args.user_id}
		frappe.log_error(f"Data validation error: {str(e)}", "Coupons get validation error")
		return create_response(BAD_REQUEST, {"message": f"Validation error: {str(e)}"})
	except frappe.ValidationError as e:
		# for user {args.user_id}
		frappe.log_error(f"Frappe validation error: {str(e)}", "Coupons get validation error")
		return create_response(BAD_REQUEST, {"message": f"Frappe validation error: {str(e)}"})
	except Exception as e:
		# for user {args.user_id}
		frappe.log_error(f"Error getting coupons: {str(e)}", "Getting Coupons Error")
		return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})

def get_items(pricing_rule):

	data = frappe.db.get_list("Pricing Rule Item Code", filters={"parent": pricing_rule}, fields=["item_code", "uom"], ignore_permissions=True,)
	if(data): 
		return data
	data = frappe.db.get_list("Pricing Rule Item Group", filters={"parent": pricing_rule}, fields=["item_group", "uom"], ignore_permissions=True,)
	if(data): 
		return data
	data = frappe.db.get_list("Pricing Rule Brand", filters={"parent": pricing_rule}, fields=["brand", "uom"], ignore_permissions=True,)
	if(data): 
		return data