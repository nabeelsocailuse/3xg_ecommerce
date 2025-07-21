import frappe
from frappe import _

def validate(doc, method):
	# Require comment if Rejected
	if doc.workflow_state == "Rejected" and not doc.remark:
		frappe.throw(_("A comment is required when rejecting a return."))

def before_submit(doc, method):
	# Block premature submission
	pass
	# if doc.requires_approval and doc.workflow_state != "Approved by CEO":
	#     frappe.throw(_("This return must be approved by the CEO before submission."))

def on_update(doc, method):
	# Auto-submit when final approval is reached
	if (
		doc.requires_approval 
		and doc.workflow_state == "Approved by CEO" 
		and doc.docstatus == 0
	):
		try:
			doc.submit()
			frappe.msgprint(_("Return has been approved and auto-submitted."))
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Auto Submit Failed")

def send_workflow_notification(doc):
	# Define map of workflow states to readable status levels
	status_map = {
		"Pending Store Manager Approval": "awaiting Store Manager's approval",
		"Pending HoS Approval": "approved by Store Manager, awaiting Head of Sales approval",
		"Pending CEO Approval": "approved by Head of Sales, awaiting CEO's approval",
		"Approved by CEO": "approved by CEO (Final Approval)",
		"Rejected by Store Manager": "rejected by Store Manager",
		"Rejected by HOS": "rejected by Head of Sales",
		"Rejected by CEO": "rejected by CEO",
	}

	# Identify message based on workflow state
	if doc.workflow_state in status_map:
		status_msg = status_map[doc.workflow_state]
		subject = f"Update on Sales Return Invoice {doc.name}"
		message = f"Your Sales Return invoice <b>{doc.name}</b> has been <b>{status_msg}</b>."

		# Email notification
		frappe.sendmail(
			recipients=[doc.owner],
			subject=subject,
			message=message,
			reference_doctype=doc.doctype,
			reference_name=doc.name
		)

		# In-app popup alert
		frappe.publish_realtime(
			event='eval_js',
			message=f"""frappe.show_alert({{
				message: "{message}",
				indicator: "{'green' if 'approved' in status_msg.lower() else 'red'}"
			}});""",
			user=doc.owner
		)

def notify_invoice_creator(doc, method=None):
	if doc.is_return and doc.requires_approval:
		send_workflow_notification(doc)



def notify_creator_on_discount_approval(doc, method):
    # Check approval condition
    if doc.workflow_state == "Approved" and doc.grand_total < doc.total:
        message = f"Your discounted Sales Invoice <b>{doc.name}</b> has been approved."

        # Create a system notification
        frappe.notify({
            "message": message,
            "recipients": [doc.owner],
            "subject": "Discount Approval Notice",
            "reference_doctype": doc.doctype,
            "reference_name": doc.name,
            "type": "Alert"
        })

        # Optional: Realtime alert on screen (if user is online)
        frappe.publish_realtime(
            event='eval_js',
            message=f"""frappe.show_alert({{
                message: `{message}`,
                indicator: "green"
            }});""",
            user=doc.owner
        )