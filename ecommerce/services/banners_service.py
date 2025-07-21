import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

def get_promotional_banners(args: dict):
	try:
		filters = frappe._dict(args)
		doctype = "Promotional Banners"
		data = frappe.db.sql("""
			Select 
				name, platform, status, banner_type, placement, height, width
			From 
				`tabPromotional Banners`
			Where 
				status="Activated"
				%s
		"""%get_conditions(filters), filters, as_dict=1)
		
		for d in data:
			d["promotional_banners_list"] = frappe.get_all("Promotional Banners Table", filters={"parent": d.name}, fields=["banner_name", "banner_image"])
		
		return create_response(SUCCESS, {"data": data})

	except ValueError as e:
		frappe.log_error(f"Data validation error", "Promotional Banners error")
		return create_response(BAD_REQUEST, {"message": f"Validation error: {str(e)}"})
	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error: {str(e)}", "Promotional Banners error")
		return create_response(BAD_REQUEST, {"message": f"Frappe validation error: {str(e)}"})
	except Exception as e:
		frappe.log_error(f"Error creating Promotional Banners: {str(e)}", "Promotional Banners error")
		return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})

def get_conditions(filters):
	conditions = " and platform=%(platform)s " if(filters.get("platform")) else ""
	conditions += " and placement=%(placement)s " if(filters.get("placement")) else ""
	return conditions

def get_home_banners(args: dict):
	try:
		filters = frappe._dict(args)
		'''
			doctype1 = "Home Banners 3XG"
			doctype2 = "Home Row1 Sliders"
			doctype3 = "Home Row3 Sliders"
		'''
		_args_ = frappe._dict({
				"home_row1_sliders": [],
				"home_row1_column3_top": {'banner_image': '', 'url': ''},
				"home_row1_column3_bottom": {'banner_image': '', 'url': ''},
				"home_row2_column1_left": {'banner_image': '', 'url': ''},
				"home_row2_column1_right": {'banner_image': '', 'url': ''},			
				"home_row3_sliders": [],
				"home_row4": {'banner_image': '', 'url': ''},
			})

		for row in  frappe.db.sql("""
				Select 
					name, platform, banner_type, status,
					ifnull(home_row1_column3_top,'') as home_row1_column3_top,
					ifnull(home_row1_column3_top_url, '') as home_row1_column3_top_url,
					ifnull(home_row1_column3_bottom, '') as home_row1_column3_bottom,
					ifnull(home_row1_column3_bottom_url, '') as home_row1_column3_bottom_url,
					ifnull(home_row2_column1_left, '') as home_row2_column1_left,
					ifnull(home_row2_column1_left_url, '') as home_row2_column1_left_url,
					ifnull(home_row2_column1_right, '') as home_row2_column1_right,
					ifnull(home_row2_column1_right_url, '') as home_row2_column1_right_url,
					ifnull(home_row4, '') as home_row4,
					ifnull(home_row4_url, '') as home_row4_url

				From 
					`tabHome Banners 3XG`
				Where 
					status="Activated"
					%s
			"""%get_conditions(filters), filters, as_dict=1):
			_args_.update({
				"home_row1_sliders": frappe.db.sql(f"Select (idx) as row, ifnull(banner_name,'') as banner_name, ifnull(banner_image,'') as banner_image, ifnull(url, '') as url from `tabHome Row1 Sliders` where parent='{row.name}' order by idx", as_dict=1),
				"home_row1_column3_top": {'banner_image': row.home_row1_column3_top, 'url': row.home_row1_column3_top_url},
				"home_row1_column3_bottom":  {'banner_image': row.home_row1_column3_bottom, 'url': row.home_row1_column3_bottom_url},
				"home_row2_column1_left":  {'banner_image': row.home_row2_column1_left, 'url': row.home_row2_column1_left_url},
				"home_row2_column1_right":  {'banner_image': row.home_row2_column1_right, 'url': row.home_row2_column1_right_url},
				"home_row3_sliders": frappe.db.sql(f"Select (idx) as row, ifnull(banner_name,'') as banner_name, ifnull(banner_image,'') as banner_image, ifnull(url, '') as url from `tabHome Row3 Sliders` where parent='{row.name}' order by idx", as_dict=1),
				"home_row4":  {'banner_image': row.home_row4, 'url': row.home_row4_url},
			})
			
		
		return create_response(SUCCESS, {"data": _args_})

	except ValueError as e:
		frappe.log_error(f"Data validation error", "Home Banners error")
		return create_response(BAD_REQUEST, {"message": f"Validation error: {str(e)}"})
	except frappe.ValidationError as e:
		frappe.log_error(f"Frappe validation error: {str(e)}", "Home Banners error")
		return create_response(BAD_REQUEST, {"message": f"Frappe validation error: {str(e)}"})
	except Exception as e:
		frappe.log_error(f"Error creating Home Banners: {str(e)}", "Home Banners error")
		return create_response(SERVER_ERROR, {"message": f"An unexpected error occurred: {str(e)}"})
