import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response
# from ecommerce.services.product_service import add_new_item

@frappe.whitelist(allow_guest=True)
def add_item(**kwargs):
    return add_new_item(kwargs)

### Add new item
def add_new_item(
    args: dict
):
    args = frappe._dict(args)
    
    def get_arguements():
        return {
            "doctype": "Products",
            "merchant_id": args.merchant_id,
            "product_name": args.product_name,
            "category": args.category,
            "brand": args.brand,
            "model": args.model,
        }         
    
    def arrange_specifications():
        spec_obj = []
        if args.specifications:
            for row in args.specifications:
                for key, value in row.items():
                    spec_obj.append({"key": key, "value": value})
        return spec_obj
    
    def arrange_colors():
        if args.color:
            return [{"color": col} for col in (args.color)]            
    
    try:
        _args_ = get_arguements()
        if frappe.db.exists(_args_):
            return create_response(SUCCESS, f"Item with provided detail already exist.")
        else:
            _args_.update({
                "merchant_id": args.merchant_id,
                "product_name": args.product_name,
                "category": args.category,
                "actual_price": args.actual_price,
                "discounted_price": args.discounted_price,
                "discount": args.discount,
                "image": args.image,
                "rating": args.rating,
                "description": args.description,
                "specifications": arrange_specifications(),
                "color": arrange_colors(),
                "quantity": args.quantity,
                "availability": args.availability,
                "collection": args.collection,
                "weight": args.weight,
                "warranty": args.warranty,
            }) 
            doc = frappe.get_doc(_args_)
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return create_response(SUCCESS, f"Item with id: '{doc.item_code}' added successfully.")

    except ValueError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(f"Error adding new item: {str(e)}", "Add Item Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


@frappe.whitelist(allow_guest=True)
def update_item(**kwargs):
    return update_product(kwargs)

### Update existing item
def update_product(args: dict):
    args = frappe._dict(args)
    
    def arrange_specifications():
        spec_obj = []
        if args.specifications:
            for row in args.specifications:
                for key, value in row.items():
                    spec_obj.append({"key": key, "value": value})
        return spec_obj
    
    def arrange_colors():
        if args.color:
            return [{"color": col} for col in (args.color)]            
    
    try:
        if (not frappe.db.exists("Products", {"item_code": args.item_code})):
            return create_response(NOT_FOUND, {
                "message": f"Item with code '{args.item_code}' not found.",
                "data": []
            })
        else:
            doc = frappe.get_doc("Products", {"item_code": args.item_code})
            doc.merchant_id= args.merchant_id
            doc.product_name= args.product_name
            doc.category= args.category
            doc.actual_price= args.actual_price
            doc.discounted_price= args.discounted_price
            doc.discount= args.discount
            doc.image= args.image
            doc.rating= args.rating
            doc.description= args.description
            doc.set("pecifications", arrange_specifications())
            doc.set("color", arrange_colors())
            doc.quantity= args.quantity
            doc.availability= args.availability
            doc.collection= args.collection
            doc.weight= args.weight
            doc.warranty= args.warranty
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            return create_response(SUCCESS, {
                "message": f"Item updated successfully!",
                "data": doc
            })

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(f"Error updating item with code '{args.item_code}': {str(e)}", "Update Product Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


@frappe.whitelist(allow_guest=True)
def get_seller_performance(user_id, seller_id):
    
    try:
        if(frappe.db.exists("User", user_id)):
            data = frappe.db.sql(""" 
                Select 
                    idt.seller_id, idt.seller_name, sum(idt.quantity) as selling_qty,  
                    (Select sum(quantity) as actual_qty From `tabProducts` Where docstatus=0 and merchant_id = idt.seller_id) as actual_qty
                From 
                    `tabOrder` odr inner join `tabOrder Item` idt on (odr.name=idt.parent)
                Where 
                    odr.docstatus=0 
                    and idt.seller_id = %(seller_id)s
                """, {"seller_id": seller_id}, 
                as_dict=True)
            
            performance_dict= {}
            for d in data:
                performance_dict.update({
                    "seller_name": d.seller_name, 
                    "percentage": round((d.selling_qty/d.actual_qty) * 100, 2) 
                })
            return create_response(SUCCESS, {"message": "User found.", "body": performance_dict})
        else:
            return create_response(NOT_FOUND, {"message": "User not found.", "data": []})
    except Exception as e:
        return create_response(SERVER_ERROR, f"{e}")


@frappe.whitelist(allow_guest=True)
def testwebhooks(**kwargs):
    print('working: ', kwargs)