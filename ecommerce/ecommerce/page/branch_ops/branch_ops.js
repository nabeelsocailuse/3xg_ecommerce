frappe.pages['branch-ops'].on_page_load = function(wrapper) {
  console.log("Branch Ops page loaded!");

  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: 'Branch Operations',
    single_column: true
  });

  // Inline CSS styling // initial colour of buttons #B22222
  const style = document.createElement('style');
  style.textContent = `
    .banner {
      background-image: url('https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1350&q=80');
      background-size: cover;
      background-position: center;
      padding: 20px;
	margin-top: -10px;
      color: white;
	height: 300px;
	
    }
    .banner h3, .banner h4 {
      text-shadow: 1px 1px 2px #fff;
    }
    .custom-btn {
      background-color: #e7906b;
      color: white;
      font-size: 16px;
      padding: 15px;
      border-radius: 8px;
      width: 100%;
      transition: background-color 0.3s ease;
      display: block;
      text-align: center;
      text-decoration: none;
    }
    .custom-btn:hover {
      background-color: #8B0000;
      color: #fff;
    }
    .module-sidebar {
      padding: 15px;
      background-color: #f8f9fa;
      border-radius: 8px;
      height: 100%;
      overflow-y: auto;
      max-height: 400px;
    }
    .module-sidebar h5 {
      font-weight: bold;
      margin-bottom: 10px;
    }
    .module-sidebar ul {
      list-style-type: none;
      padding: 0;
    }
    .module-sidebar li {
      margin: 8px 0;
    }
    .module-sidebar a {
      text-decoration: none;
      color: #343a40;
    }
    .module-sidebar a:hover {
      text-decoration: underline;
    }
  `;
  document.head.appendChild(style);

  // Define button data
  const buttons = [
    { label: "My Profile", route: "/app/employee?user_id=" },
    { label: "Salary Slip", route: "/app/salary-slip" },
    { label: "Leave Application", route: "/app/leave-application" },
    { label: "Expense Advance", route: "/app/expense-claim" },
    { label: "Material Requisition", route: "/app/material-request" },
    { label: "Warehouse-Wise Age & Value", route: "/app/query-report/Warehouse%20wise%20Item%20Balance%20Age%20and%20Value" },
    { label: "Sales Invoice", route: "/app/sales-invoice/view/list" },
    { label: "Stock Ledger", route: "/app/query-report/Stock%20Ledger" },
    { label: "Point of Sale", route: "/app/posapp" },
  ];

  // Generate button HTML
  const buttonsHTML = buttons.map(btn => `
    <div class="col-md-4 my-2">
      <a href="${btn.route}" class="custom-btn">${btn.label}</a>
    </div>
  `).join("");

  // Sidebar workspace modules
  const workspaces = frappe.boot?.workspaces || [];
  const sidebarHTML = workspaces.length > 0
    ? `
    <div class="module-sidebar">
      <h5>Workspaces</h5>
      <ul>
        ${workspaces.map(ws => `<li><a href="/app/${ws.module}">${ws.label}</a></li>`).join("")}
      </ul>
    </div>
  ` : "";

  // Main content
  const html = document.createElement("div");
  html.innerHTML = `
<div class="banner text-center rounded mb-4">
        <h3>${frappe.session.user_fullname}</h3>
        <h4 id="clock">--:--:--</h4>
      </div>
    <div class="container my-4">
      
      <div class="container my-4">
        <div class="col-md-3">
          ${sidebarHTML}
        </div>
        <div class="container my-4">
          <div class="row">
            ${buttonsHTML}
          </div>
        </div>
      </div>
    </div>
  `;

  // Append HTML to page
  page.container.append(html);

  // Clock updater
  function updateClock() {
    const clock = document.getElementById('clock');
    if (clock) {
      const now = new Date();
      clock.innerText = now.toLocaleTimeString();
    }
  }

  updateClock();
  setInterval(updateClock, 1000);
};
