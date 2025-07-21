import frappe
from frappe.utils import fmt_money, format_date

@frappe.whitelist()
def get_order_stats():
	order_dict = {}
	totals = get_order_totals()
	order_dict.update(totals)
	order_dict.update({"orders": get_order_list()})
	return order_dict

def get_order_totals():
	orders = frappe.db.sql("""
		Select 
			count(status) as total, status
		From
			`tabOrder`
		Group by 
			status
		""", as_dict=1)
	statuses = {
		"ongoing": 0,
		"pending": 0,
		"completed": 0,
		"rejected": 0
	}
	
	for d in orders:
		if(d.status=="Ongoing"):
			statuses.update({"ongoing": d.total})
		elif(d.status=="Pending"):
			statuses.update({"pending": d.total})
		elif(d.status=="Completed"):
			statuses.update({"completed": d.total})
		elif(d.status=="Rejected"):
			statuses.update({"rejected": d.total})

	return statuses

def get_order_list():
	data = frappe.db.sql("""
		Select 
			name, email, order_id, status, (net_total) as order_price, cast(creation as date) as creation_date, shipping_address 
		From
			`tabOrder`
		Order by
			creation desc
		""", as_dict=1)
	
	for d in data:
		d["order_price"] = fmt_money(d.order_price, currency="NGN")
		d["creation_date"] = format_date(d.creation_date, "dd-MMM-YYYY")
	return data