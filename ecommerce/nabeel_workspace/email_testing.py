import frappe

from frappe.core.doctype.communication.email import make

# bench --site zirconprod.3xg.africa execute ecommerce.nabeel_workspace.email_testing.sending
@frappe.whitelist(allow_guest=True)
def sending():
	comm = make(
			doctype="Email Group Member",
			name="vll9kkuls3",
			subject="You’re In! Welcome to 3xG’s Inner Circle",
			content="<p>Let’s make this launch epic—tell us what you’re eyeing!</p>",
			sender="support@3xg.africa",
			recipients=["nabeel.s@3xg.africa"],
			communication_medium="Email",
			sent_or_received="Sent",
			send_email=True,
			email_template="Welcome Waitlist",
		)
	frappe.db.commit()
	return comm