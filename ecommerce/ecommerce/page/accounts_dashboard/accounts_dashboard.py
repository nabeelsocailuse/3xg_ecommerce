import frappe
from frappe.utils import fmt_money, format_date

@frappe.whitelist()
def get_order_stats():
	order_dict = {}
	totals = get_totals()
	order_dict.update(totals)
	order_dict.update({"transactions": get_transactions_list()})
	order_dict.update({"product_wise_commission": get_product_wise_commission_list()})
	return order_dict

def get_totals():
	accounts_list = {
		"commission_balance": "0007 - Commission on Sales - 3E",
		"merchant_balance": "1121 - Merchant Account - 3E",
		"delivery_charges": "5208 - Shipping and Delivery charges - 3E",
		"wallet_balance": "1001 - Wallet Account - 3E",
	}
	balances = {
		"commission_balance": fmt_money(0, currency="NGN"),
		"merchant_balance": fmt_money(0, currency="NGN"),
		"delivery_charges": fmt_money(0, currency="NGN"),
		"wallet_balance": fmt_money(0, currency="NGN"),
	}
	for key, value in accounts_list.items():
		amount = frappe.db.sql(f"""
			Select 
				sum(credit-debit) as total
			From
				`tabAccounting Transactions`
			Where account = '{value}'
			""", as_dict=0)
		if(amount): balances[key] = fmt_money(amount[0][0], currency="NGN")  

	return balances

def get_transactions_list():
	data = frappe.db.sql("""
		Select posting_date, account, party_type, party, item_name, sum(credit) as credit, sum(debit) as debit, sum(credit-debit) balance
		From `tabAccounting Transactions`
		Group by account
		Order by account
		""", as_dict=1)
	
	for d in data:
		d["credit"] = fmt_money(d.credit, currency="NGN")
		d["debit"] = fmt_money(d.debit, currency="NGN")
		d["balance"] = fmt_money(d.balance, currency="NGN")
		d["posting_date"] = format_date(d.posting_date, "dd-MMM-YYYY")
	
	return data

def get_product_wise_commission_list():
	data = frappe.db.sql("""
		Select (item_code) as product_code, (item_name) as product_name, sum(credit) as commission_amount
		From `tabAccounting Transactions`
		Where ifnull(item_code, "")!=""
		Group by item_code
		""", as_dict=1)
	
	for d in data:
		d["commission_amount"] = fmt_money(d.commission_amount, currency="NGN")
	
	return data