import frappe
from frappe.utils import nowdate, getdate
from frappe import _


def mark_requires_approval_on_return(doc, method):
	if doc.is_return and not doc.requires_approval:
		doc.requires_approval = 1
		doc.workflow_type = "Return"

def assign_workflow_type(doc, method):
	"""Set workflow_type based on whether it's a return or discounted invoice."""
	total_discount = sum([item.discount_amount or 0 for item in doc.items])

	if doc.is_return:
		doc.workflow_type = "Return"
	elif total_discount > 0:
		doc.workflow_type = "Discount"
	else:
		doc.workflow_type = "Normal"  # Fallback default


#and doc.docstatus == 0
def intercept_return_submission(doc, method):
	if doc.is_return and doc.workflow_state != "Approved by CEO":
		frappe.throw(
			_("This Sales Return must be fully approved before submission."),
			title="Approval Required"
		)

def restore_invoice_status_on_submit(doc, method):
	pass
	# if not doc.is_return and doc.docstatus == 1:
	#     if doc.outstanding_amount == 0:
	#         doc.db_set("status", "Paid")
	#     elif doc.due_date and doc.due_date < getdate(nowdate()):
	#         doc.db_set("status", "Overdue")
	#     else:
	#         doc.db_set("status", "Partly Paid")




#def flag_discounted_invoices(doc, method):
#	total_discount = sum([item.discount_amount or 0 for item in doc.items])
#	if total_discount > 0:
#		doc.requires_discount_approval = 1
#		doc.workflow_type = "Discount"

def flag_discounted_invoices(doc, method):
	total_discount = sum([item.discount_amount or 0 for item in doc.items])

	if total_discount > 0:
		doc.requires_discount_approval = 1
		doc.workflow_type = "Discount"

		# Protect paid_amount from getting lost
		if doc.get("paid_amount") and not doc.get("temp_paid_amount"):
			doc.temp_paid_amount = doc.paid_amount


#def block_discount_submission(doc, method):
    # Total discounts on invoice
 #   total_discount = sum([d.discount_amount or 0 for d in doc.items])
	
    # Check if discount applied AND if not already approved in workflow
  #  if total_discount > 0 and doc.workflow_state != "Approved by CEO":
   #     frappe.throw(_("Discounted invoices require approval before submission."), title="Approval Required")


def block_discount_submission(doc, method):
	total_discount = sum([item.discount_amount or 0 for item in doc.items])

	# If discount is applied and no workflow has auto-submitted, prevent manual submission
	#not frappe.flags.in_workflow
	if total_discount > 0 and doc.workflow_state != "Approved by CEO":
		frappe.throw(
			_("You can't submit a discounted invoice directly. It must go through the approval process."),
			title="Approval Required"
		)
