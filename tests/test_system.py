from src.menu_manager import MenuManager
from src.cart import Cart
from src.order_manager import OrderManager
from src.kitchen_queue import KitchenQueue

def main():
    menu=MenuManager(); assert menu.count_products()>=6
    latte=menu.get_product("latte"); cart=Cart(); cart.add_item(latte,2,{"size":"Medium","temperature":"Iced","sugar":"Low","milk":"Oat","toppings":["Caramel"],"extra_price":.8})
    assert cart.get_item_count()==2 and cart.get_total()>0
    om=OrderManager(); order=om.create_order(cart); assert order.status=="PENDING"
    k=KitchenQueue(om); k.start_order(order.order_id); assert order.status=="PREPARING"; k.mark_order_ready(order.order_id); assert order.status=="READY"
    print("SYSTEM TEST PASSED",order.order_id,f"${order.total:.2f}")
if __name__=="__main__": main()
