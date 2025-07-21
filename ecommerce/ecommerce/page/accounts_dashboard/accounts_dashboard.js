frappe.pages['accounts-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Accounts Dashboard',
		single_column: true
	});

    frappe.call({
        method: 'ecommerce.ecommerce.page.accounts_dashboard.accounts_dashboard.get_order_stats',
        callback: function(r) {
            if (r.message) {
                const data = r.message;
                const html = frappe.render_template("accounts_dashboard", data);
                $(html).appendTo(page.body);
                
                setTimeout(() => {
                    if ($('#example').length) {
                        $('#example').DataTable({
                            pageLength: 10,
                            // columns: [
                            //     { searchable: true },   // Column 1
                                
                            // ]
                        });
                    } else {
                        console.error("Table with ID #example not found.");
                    }
                }, 100);
                setTimeout(() => {
                    if ($('#productId').length) {
                        $('#productId').DataTable({
                            pageLength: 10,
                            // columns: [
                            //     { searchable: true },   // Column 1
                                
                            // ]
                        });
                    } else {
                        console.error("Table with ID #productId not found.");
                    }
                }, 100);
            }
        }
    });
};


