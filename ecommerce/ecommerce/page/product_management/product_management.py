import frappe
from frappe.utils import fmt_money, format_date

@frappe.whitelist()
def get_product_stats():
	product_dict = {}
	totals = get_product_totals()
	product_dict.update(totals)
	product_dict.update({"products": get_product_list()})
	return product_dict

#retrieve products based on their groups - for Dashboard Cards
def get_product_totals():
	products = frappe.db.sql("""
		Select 
			count(status) as total, status
		From
			`tabProducts`
		Group by 
			status
		""", as_dict=1)

	is_disabled = frappe.db.count('Products', {'is_disabled': 0})
	

	statuses = {
		"live": 0,
		"in_review": 0,
		"disabled": 0,
        	"is_disabled": is_disabled
	}
	
	for d in products:
		if(d.status=="LIVE"):
			statuses.update({"live": d.total})
		elif(d.status=="IN_REVIEW"):
			statuses.update({"in_review": d.total})
		elif(d.status=="DISABLED"):
			statuses.update({"disabled": d.total})
        	
		
	return statuses

def get_context(context):
    # Get product totals
    context.statuses = get_product_totals()
	
#retrieves specific fields related to Products
def get_product_list():
	data = frappe.db.sql("""
		Select 
			item_code, name, product_name, actual_price, discounted_price, owner, merchant_email, status, cast(creation as date) as creation,  modified, created_at


		From
			`tabProducts`
		Order by
			creation desc
		""", as_dict=1)
	
	for d in data:
		d["actual_price"] = fmt_money(d.actual_price, currency="NGN")
		d["creation"] = format_date(d.creation, "dd-MMM-YYYY")
		d["modified"] = format_date(d.modified, "dd-MMM-YYYY")
	return data