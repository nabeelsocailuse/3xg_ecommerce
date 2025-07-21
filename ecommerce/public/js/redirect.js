document.addEventListener('DOMContentLoaded', function() {
    console.log("redirect.js loaded");

    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "User",
            name: frappe.session.user
        },
        callback: function(r) {
            console.log("User roles fetched:", r.message ? r.message.roles : "No roles");
            if (r.message) {
                const roles = r.message.roles.map(r => r.role);
                if (roles.includes("Cashiers")) {
                    console.log("Redirecting user to custom page");
                    if (!window.location.pathname.includes("/app/branch-ops")) {
                        window.location.href = "/app/branch-ops";
                    }
                }
            }
        }
    });
});
