// Copyright (c) 2025, 3XG and contributors
// For license information, please see license.txt

frappe.ui.form.on('XG Accounts Settings', {
	refresh: function(frm) {
		frm.set_query('physical_warehouse', function() {
			return {
				filters: {
					is_group: 0,
					company: frm.doc.company
				}
			}
		});
		frm.set_query('virtual_warehouse', function() {
			return {
				filters: {
					is_group: 0,
					company: frm.doc.company
				}
			}
		});

		frm.set_query('merchant_account', function() {
			return {
				filters: {
					is_group: 0,
					disabled: 0,
					company: frm.doc.company
				}
			}
		});
		frm.set_query('wallet_account', function() {
			return {
				filters: {
					is_group: 0,
					disabled: 0,
					company: frm.doc.company
				}
			}
		});

		frm.set_query('shipping_account', function() {
			return {
				filters: {
					is_group: 0,
					disabled: 0,
					company: frm.doc.company
				}
			}
		});
		frm.set_query('commission_account', function() {
			return {
				filters: {
					is_group: 0,
					disabled: 0,
					company: frm.doc.company
				}
			}
		});
	},
	company: function(frm){
		frm.set_value('physical_warehouse', '');
		frm.set_value('virtual_warehouse', '');
		frm.set_value('wallet_account', '');
		frm.set_value('shipping_account', '');
		frm.set_value('merchant_account', '')
	}
});
