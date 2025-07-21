# Copyright (c) 2025, 3XG and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class WalletTransaction(Document):

	def after_insert(self):
		frappe.enqueue(
			make_accounting_entries,
			timeout=300,
			self = self,
			publish_progress=False,
		)


def make_accounting_entries(self, publish_progress=False):
	args =  frappe._dict({
		'doctype': 'Accounting Transactions',
		'posting_date': getdate(),
		'party_type': 'Website User',
		'party': self.email,
		'against': 'Wallet Transaction',
		'voucher_type': 'Wallet Transaction',
		'voucher_no': self.name,
		'remarks': 'Wallet balance added',
		'company': self.company,
		'due_date': getdate(),
		'is_cancelled': 0,
	})
	# Wallet Account Entry
	args.update({
    	'account': self.wallet_account,
		'credit': self.amount
	})
	frappe.get_doc(args).insert(ignore_permissions=True)
	# Wallet Funding Fee Account Entry
	args.update({
		'account': self.wallet_funding_fee_account,
		'credit': self.fee
	})
	frappe.get_doc(args).insert(ignore_permissions=True)
