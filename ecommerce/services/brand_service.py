import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_brands():
   
    try:
        query = """
            SELECT *
            FROM `tabProduct Brand`
            WHERE 1=1
        """
         
        brands = frappe.db.sql(query, as_dict=True)

        if not brands:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, brands)

    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching brands")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    
    

def get_single_brand(name):
    try:
        query = """
            SELECT *
            FROM `tabProduct Brand`
            WHERE name = %s
        """
        
        brand = frappe.db.sql(query, (name,), as_dict=True)

        if not brand:
            return create_response(NOT_FOUND, [])

        return create_response(SUCCESS, brand)

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching brand")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

    

# Nabeel Saleem, 23-12-2024
def get_best_selling_brands(category, brand, model, date):
    
    try:
        def get_select_clause():
            select ="" 
            if(category): select += f"p.category,"
            if(brand): select += f"p.brand,"
            if(model): select += f"p.model,"
            if(select==""): select = f"p.brand,"
            return select
        
        def get_where_clause():
            """ where = f" and p.category='{category}' " if(category) else ""
            where += f" and p.brand='{brand}' " if(brand) else ""
            where += f" and p.model='{model}' " if(model) else "" """
            where = f" and YEAR(od.creation)=YEAR('{date}') and MONTH(od.creation)=MONTH('{date}') " if(date) else ""
            return where
        def get_group_by_clause():
            group_list = []
            if(category): group_list += ["p.category"]
            if(brand): group_list += ["p.brand"]
            if(model): group_list += ["p.model"]
            group_by = " Group By %s "%(",".join(group_list)) if(group_list) else " Group By p.brand"
            return group_by
        
        brands_list = frappe.db.sql(f""" 
            SELECT 
                p.*, {get_select_clause()} sum(ot.quantity) as qty
            FROM 
                `tabOrder` od
            INNER JOIN 
                `tabOrder Item` ot ON od.name = ot.parent
            INNER JOIN 
                `tabProducts` p ON ot.item_code = p.item_code
            Where od.docstatus=0
            {get_where_clause()}
            {get_group_by_clause()}
            Order by
                qty desc; """, as_dict=1)    
        return create_response(SUCCESS, brands_list)
    except frappe.DoesNotExistError as e:
        return create_response(SUCCESS, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching brands")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")