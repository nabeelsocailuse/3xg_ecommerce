import frappe
from frappe.utils import fmt_money, format_date

@frappe.whitelist()
def get_product_stats():
	product_dict = {}
	totals = get_product_totals()
	product_dict.update(totals)
	product_dict.update({"products": get_product_list()})
	return product_dict


def get_product_totals():
	products = frappe.db.sql("""
		SELECT 
			COUNT(*) AS total,
			SUM(CASE WHEN status = 'Applied' THEN 1 ELSE 0 END) AS applied,
			SUM(CASE WHEN status = 'Activated' THEN 1 ELSE 0 END) AS activated,
			SUM(CASE WHEN status = 'Deactivated' THEN 1 ELSE 0 END) AS deactivated
		FROM `tabMerchants`
	""", as_dict=1)[0]

	#docstatus = frappe.db.count('Merchants', {'docstatus': 0})

	return {
		"total": products.total or 0,
		"applied": products.applied or 0,
		"activated": products.activated or 0,
		"deactivated": products.deactivated or 0,
	}


def get_context(context):
	context.statuses = get_product_totals()


def get_product_list():
	data = frappe.db.sql("""
		SELECT 
			m.name,
			m.merchant_id,
			m.business_name,
			m.full_name,
			m.email,
			m.status,
			m.owner,
			CAST(m.creation AS DATE) AS creation,
			m.modified,
			IFNULL(w.amount, 0) AS wallet_balance
		FROM `tabMerchants` m
		LEFT JOIN `tabWallet` w ON m.merchant_id = w.merchant_id
		ORDER BY m.creation DESC
	""", as_dict=1)

	for d in data:
		d["creation"] = format_date(d.creation, "dd-MMM-YYYY")
		d["modified"] = format_date(d.modified, "dd-MMM-YYYY")
		d["wallet_balance"] = fmt_money(d.wallet_balance or 0, currency="NGN")

	return data
