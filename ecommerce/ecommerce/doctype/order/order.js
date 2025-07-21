// Copyright (c) 2024, 3XG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Order', {
	refresh: function(frm) {
		frm.set_query('debit_to_account', function(){
			return{
				filters:{
					disabled: 0,
					is_group: 0,
					company: frm.doc.company
				}
			}
		})
		frm.set_query('merchant_goods_account', function(){
			return{
				filters:{
					disabled: 0,
					is_group: 0,
					company: frm.doc.company
				}
			}
		})
		frm.set_query('wallet_account',function(){
			return{
				filters:{
					disabled: 0,
					is_group: 0,
					company: frm.doc.company
				}
			}
		})
		frm.set_query('shipping_account',function(){
			return{
				filters:{
					disabled: 0,
					is_group: 0,
					company: frm.doc.company
				}
			}
		})

		frm.set_query('commission_account',function(){
			return{
				filters:{
					disabled: 0,
					is_group: 0,
					company: frm.doc.company
				}
			}
		})
	}
});
