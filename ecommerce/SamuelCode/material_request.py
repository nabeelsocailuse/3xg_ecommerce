import frappe
import json
from frappe import _

def validate_rejection_comment(doc, method):
    if doc.workflow_state and "Reject" in doc.workflow_state:
        if not doc._comments:
            frappe.throw(_("You must add a comment before rejecting this Material Request."))

        try:
            comments = json.loads(doc._comments)
        except Exception:
            frappe.throw(_("Could not read comments. Please try again."))

        if not comments:
            frappe.throw(_("You must add a comment before rejecting this Material Request."))

        # Optional: check for a recent comment (e.g., added within the last 5 minutes)
        from datetime import datetime, timedelta
        now = frappe.utils.now_datetime()
        recent_threshold = now - timedelta(minutes=5)

        has_recent = any(
            frappe.utils.get_datetime(c.get("creation")) >= recent_threshold
            for c in comments if c.get("comment_type") == "Comment"
        )

        # if not has_recent:
        #     frappe.throw(_("You must add a recent comment (within 5 minutes) before rejecting."))

def notify_request_creator_on_approval(doc, method):
    # Adjust this to your actual final approval state name
    if doc.workflow_state == "Pending":  
        message = f"Your Material Request <b>{doc.name}</b> has been <b>approved</b>."

        # In-app alert
        # frappe.publish_realtime(
        #     event='eval_js',
        #     message=f"""frappe.show_alert({{
        #         message: "{message}",
        #         indicator: "green"
        #     }});""",
        #     user=doc.owner
        # )
        
        # Using frappe.throw to trigger the alert
        # This is a workaround to show the alert in the UI
        # as frappe.publish_realtime may not work in all contexts
        
        # frappe.throw(
        #     ("Material Request Approved"),
           
        # )
        
        try:
            frappe.publish_realtime(
                event='eval_js',
                message=f"""frappe.show_alert({{
                    message: `{message}`,
                    indicator: "green"
                }});""",
                user=doc.owner
            )
        except Exception as e:
            frappe.log_error(str(e), "Realtime alert to creator failed")
            
        # Optional: Email notification
        # frappe.sendmail(
        #     recipients=[doc.owner],
        #     subject=f"Material Request {doc.name} Approved",
        #     message=message,
        #     reference_doctype=doc.doctype,
        #     reference_name=doc.name
        # )