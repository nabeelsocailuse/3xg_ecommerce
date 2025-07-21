frappe.pages['customer-dashboard'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Customer Dashboard',
        single_column: true
    });

    frappe.call({
        method: 'ecommerce.ecommerce.page.customer_dashboard.customer_dashboard.get_customer_stats',
        callback: function(r) {
            if (r.message) {
                const data = r.message;
                const html = frappe.render_template("customer_dashboard", data);
                $(html).appendTo(page.body);

                setTimeout(() => {
                    const table = $('#example');
                    if (table.length) {
                        table.DataTable({
                            pageLength: 10
                        });
                    } else {
                        console.error("Table with ID #example not found.");
                    }
                }, 100);
            } else {
                console.error("No data returned from get_customer_stats.");
            }
        }
    });
};
