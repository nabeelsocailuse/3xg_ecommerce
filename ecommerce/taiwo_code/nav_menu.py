import frappe

@frappe.whitelist(allow_guest=True)
def get_nav_menu():
    menu = {}
    for row1 in frappe.db.sql(""" select name, image from `tabItem Group` where is_group =1 and parent_item_group = "All Item Groups" """, as_dict=1):
        print(row1)
        submenu = {}
        for row2 in frappe.db.sql(f""" Select name from `tabItem Group` where is_group =1 and parent_item_group = '{row1.name}' """, as_dict=1):
            
            subsubmenu = set()
            for row3 in frappe.db.sql(f""" Select name from `tabItem Group` where is_group =0  and parent_item_group = '{row2.name}' """, as_dict=1):
                subsubmenu.add(row3.name)
                
            submenu.update({row2.name: subsubmenu})
        submenu.update({"image": row1.image})
        menu.update({row1.name: submenu})
    
    return menu

# bench --site 3xg.africa execute ecommerce.taiwo_code.nav_menu.get_nav_menu