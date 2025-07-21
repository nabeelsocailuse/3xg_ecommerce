import frappe
from ecommerce.constants.http_status import (SUCCESS, NOT_FOUND, SERVER_ERROR)
from ecommerce.utils.response_helper import create_response
from frappe.core.doctype.communication.email import make

# 04-04-2025 Nabeel Saleem
def joining(args: dict):
	try:
		args = frappe._dict(args)

		# verify email
		if(frappe.db.exists('Email Group Member', {"email_group": "3xg Shop Waitlist", "email": args.email})):
			return create_response(SUCCESS, f"Already in waitlist <b>{args.email}</b>")
		
		# create email group member
		cargs = {

			"full_name": args.full_name,
			"email": args.email,
			"phone_number": args.phone_number,
			"service": args.service,
			"email_group": "3xg Shop Waitlist",
			"source": "Join Waitlist",
			"doctype": 'Email Group Member'
		}
		doc = frappe.get_doc(cargs)
		doc.insert(ignore_permissions=True)

		send_waitlist_welcome_email(args, doc)
		
		return create_response(SUCCESS, {
			"data": doc,
			"message": "Join waitlist successfully!"
		})

	except frappe.DoesNotExistError as e:
		return create_response(NOT_FOUND, str(e))
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=str(e), title="Error creating waitlist")
		return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

def send_waitlist_welcome_email(args, email_group_member):
	recipient_list = [
		args.email
	]

	context = args
	email_group = frappe.get_doc("Email Group", "3xg Shop Waitlist")
	
	if(email_group.welcome_email_template):
		email_template = frappe.get_doc("Email Template", email_group.welcome_email_template)
		# subject=frappe.render_template(email_template.get("subject"), context)
		content=frappe.render_template(email_template.get("response_html"), context)
		
		frappe.sendmail(
			recipients=recipient_list,
			subject=email_template.get("subject"),
			message=content,
			# args = dict(),
			# template='birthday_reminder',
			# message = "Working...",
			# header=('Join Waitlist')
		)
	# 	comm = make(
	# 		doctype="Email Group Member",
	# 		name=email_group_member.name,
	# 		subject=subject,
	# 		content=content,
	# 		sender="support@3xg.africa",
	# 		recipients=recipient_list,
	# 		communication_medium="Email",
	# 		sent_or_received="Sent",
	# 		send_email=True,
	# 		email_template=email_template.name,
	# 	)
	# return comm