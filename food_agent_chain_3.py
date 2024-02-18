from datetime import datetime

def handler(pd: "pipedream"):
    shopping_lists = pd.steps["python_1"]["$return_value"]["shopping_lists"]
    orders = []

    def generate_order_items(items):
        order_items = []
        for index, item in enumerate(items, start=1):
            order_item = {
                "line_num": str(index),
                "count": 1, 
                "special_instructions": "",
                "replacement_policy": "shoppers_choice",
                "item": {"upc": item["product_id"]}  
            }
            order_items.append(order_item)
        return order_items

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    for store, items in shopping_lists.items():
        order = {
            "order_id": f"order_{store.lower()}_{timestamp}",  
            "service_option_hold_id": 1, 
            "initial_tip_cents": 499, 
            "leave_unattended": False,
            "special_instructions": f"Deliver to front door please!  Items from {store}. Thank you",
            "location_code": store.lower(),
            "paid_with_ebt": False,
            "locale": "en-US",
            "applied_instacartplus": False,
            "user": {
                "birthday": "2003-11-05", 
                "phone_number": "+123456789",
                "sms_opt_in": True
            },
            "address": {
                "address_line_1": "459 Lagunita Drive",
                "address_line_2": "",
                "address_type": "residential",
                "postal_code": "94305"
            },
            "items": generate_order_items(items)
        }
        orders.append(order)

    return_value = {
        "orders": orders,
        "original_shopping_list": shopping_lists
    }
    
    return {"output":str(return_value).replace("'", '"')}
