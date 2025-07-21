

frappe.pages['product-management'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Product Dashboard',
        single_column: true
    });

    frappe.call({
        method: 'ecommerce.ecommerce.page.product_management.product_management.get_product_stats',
        callback: function(r) {
            if (r.message) {
                const data = r.message;
                const html = frappe.render_template("product_management", data);
                $(html).appendTo(page.body);
                
                setTimeout(() => {
                    if ($('#example').length) {
                        $('#example').DataTable({
                            pageLength: 10
                        });
                    } else {
                        console.error("Table with ID #example not found.");
                    }
                }, 100);
            }
        }
    });
};


