import frappe
from frappe.utils import fmt_money, format_date

@frappe.whitelist()
def get_product_stats():
    product_dict = {}
    totals = get_product_totals()

    # Flatten totals for HTML use
    product_dict.update({
        "completed": f'{totals["completed"]["amount"]}  ({totals["completed"]["count"]}) transactions',
        "pending": f'{totals["pending"]["amount"]}  ({totals["pending"]["count"]}) transactions',
        "rejected": f'{totals["rejected"]["amount"]} ({totals["rejected"]["count"]}) transactions',
        "docstatus": totals["docstatus"],
        "total_amount": totals["total_amount"]
    })

    product_dict.update({"products": get_product_list()})
    return product_dict


def get_product_totals():
    products = frappe.db.sql("""
        SELECT 
            status,
            SUM(amount) AS total_amount,
            COUNT(*) AS count
        FROM
            `tabTransaction`
        GROUP BY 
            status
    """, as_dict=1)

    docstatus = frappe.db.count('Transaction', {'docstatus': 0})

    # Initialize totals
    total_all_amount = 0

    statuses = {
        "completed": {"amount": 0, "count": 0},
        "pending": {"amount": 0, "count": 0},
        "rejected": {"amount": 0, "count": 0},
        "docstatus": docstatus,
        "total_amount": "?0.00"
    }

    for d in products:
        status_key = d.status.lower()
        if status_key in statuses:
            amount = d.total_amount or 0
            statuses[status_key]["amount"] = fmt_money(amount, currency="NGN")
            statuses[status_key]["count"] = d.count or 0
            total_all_amount += amount

    statuses["total_amount"] = fmt_money(total_all_amount, currency="NGN")
    return statuses


def get_context(context):
    # Get product totals
    context.statuses = get_product_totals()
	
#retrieves specific fields related to Products
def get_product_list():
	data = frappe.db.sql("""
		Select 
			 name, owner, transaction_type, payment_provider, user_id, amount, status, fees, cast(creation as date) as creation,  modified, created_at


		From
			`tabTransaction`
		Order by
			creation desc
		""", as_dict=1)
	
	for d in data:
		d["actual_price"] = fmt_money(d.actual_price, currency="NGN")
		d["creation"] = format_date(d.creation, "dd-MMM-YYYY")
		d["modified"] = format_date(d.modified, "dd-MMM-YYYY")
	return data