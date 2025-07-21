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
			`tabPayout Request`
		Group by 
			status
		""", as_dict=1)

	total_count = frappe.db.count('Payout Request')
	

	statuses = {
		"approved": 0,
		"in_review": 0,
		"rejected": 0,
        	"total": total_count
	}
	
	for d in products:
		if(d.status=="Approved"):
			statuses.update({"approved": d.total})
		elif(d.status=="In Review"):
			statuses.update({"in_review": d.total})
		elif(d.status=="Rejected"):
			statuses.update({"rejected": d.total})
        	
		
	return statuses

def get_context(context):
    # Get product totals
    context.statuses = get_product_totals()
	
#retrieves specific fields related to Products
def get_product_list():
	data = frappe.db.sql("""
		Select 
			 name, merchant_fullname, owner, merchant_email, business_name, amount, status, cast(creation as date) as creation,  modified


		From
			`tabPayout Request`
		Order by
			creation desc
		""", as_dict=1)
	
	for d in data:
		d["actual_price"] = fmt_money(d.actual_price, currency="NGN")
		d["creation"] = format_date(d.creation, "dd-MMM-YYYY")
		d["modified"] = format_date(d.modified, "dd-MMM-YYYY")
	return data