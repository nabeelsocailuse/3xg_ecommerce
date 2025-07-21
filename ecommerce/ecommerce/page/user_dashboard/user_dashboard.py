import frappe
from frappe.utils import fmt_money, format_date

@frappe.whitelist()
def get_customer_stats():
	customer_dict = {}
	totals = get_customer_totals()
	customer_dict.update(totals)
	customer_dict.update({"customers": get_customer_list()})
	return customer_dict


def get_customer_totals():
	customers = frappe.db.sql("""
		SELECT 
			COUNT(*) AS total,
			SUM(CASE WHEN disabled = 0 THEN 1 ELSE 0 END) AS enabled,
			SUM(CASE WHEN disabled = 1 THEN 1 ELSE 0 END) AS disabled
		FROM `tabCustomer`
	""", as_dict=1)[0]

	return {
		"total": customers.total or 0,
		"enabled": customers.enabled or 0,
		"disabled": customers.disabled or 0,
	}


def get_context(context):
	context.statuses = get_customer_totals()


def get_customer_list():
	data = frappe.db.sql("""
		SELECT 
			name,
			customer_name,
			customer_type,
			email_id,
			disabled,
			owner,
			CAST(creation AS DATE) AS creation,
			modified
		FROM `tabCustomer`
		ORDER BY creation DESC
	""", as_dict=1)

	for d in data:
		d["creation"] = format_date(d.creation, "dd-MMM-YYYY")
		d["modified"] = format_date(d.modified, "dd-MMM-YYYY")
		d["account_status"] = "Enabled" if d.disabled == 0 else "Disabled"

	return data
