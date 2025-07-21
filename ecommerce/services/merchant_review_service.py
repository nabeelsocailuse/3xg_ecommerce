import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response


def create_merchant_review(merchant_id, rating, comment):
    try:
        if not (1 <= float(rating) <= 5):
            return create_response(
                BAD_REQUEST, "Rating must be a valid float between 1 and 5."
            )

        merchant = frappe.get_doc("Merchant", {"merchant_id": merchant_id})

        if not merchant:
            return create_response(NOT_FOUND, [])

        review = frappe.get_doc({
            "doctype": "Merchant Review",
            "merchant_id": merchant_id,
            "rating": float(rating),
            "comment": comment,
            "status": "Pending"
        })
        review.insert()
        frappe.db.commit()

        return create_response(SUCCESS, {
            "message": "Merchant review submitted successfully and is pending approval."
        })

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error creating merchant review")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")




def list_reviews(merchant_id):
    try:
        query = """
            SELECT rating, comment
            FROM `tabMerchant Review`
            WHERE merchant_id = %s
        """
        
        reviews = frappe.db.sql(query, (merchant_id,), as_dict=True)

        if not reviews:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, reviews)

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching reviews")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def get_average_rating(merchant_id):
    try:
        if not frappe.db.exists("Merchants", {"merchant_id": merchant_id}):
            return create_response(
                NOT_FOUND,
                {"message": f"Merchant with ID '{merchant_id}' does not exist."}
            )

        query = """
            SELECT COALESCE(AVG(rating), 0) AS average_rating
            FROM `tabMerchant Review`
            WHERE merchant_id = %s
        """
        result = frappe.db.sql(query, (merchant_id,), as_dict=True)
        average_rating = result[0]["average_rating"] if result else 0

        formatted_average_rating = float(f"{average_rating:.1f}")

        return create_response(SUCCESS, {
            "message": "Average rating fetched successfully.",
            "average_rating": formatted_average_rating
        })

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching merchant average rating")
        return create_response(SERVER_ERROR, {
            "message": f"An unexpected error occurred: {str(e)}"
        })


