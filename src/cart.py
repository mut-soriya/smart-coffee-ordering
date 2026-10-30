class CartItem:
    def __init__(self,product,quantity=1,customization=None): self.product=product; self.quantity=max(1,int(quantity)); self.customization=customization or {}
    def get_unit_price(self): return self.product.price+float(self.customization.get("extra_price",0))
    def get_subtotal(self): return self.get_unit_price()*self.quantity
    def to_dict(self): return {"product":self.product.to_dict(),"quantity":self.quantity,"customization":self.customization.copy(),"subtotal":self.get_subtotal()}

class Cart:
    def __init__(self): self.items=[]
    def add_item(self,product,quantity=1,customization=None):
        customization=customization or {}
        for item in self.items:
            if item.product.product_id==product.product_id and item.customization==customization: item.quantity+=quantity; return item
        item=CartItem(product,quantity,customization); self.items.append(item); return item
    def remove_item(self,index):
        if 0<=index<len(self.items): return self.items.pop(index)
    def update_quantity(self,index,delta):
        if 0<=index<len(self.items): self.items[index].quantity=max(1,self.items[index].quantity+delta); return self.items[index]
    def update_customization(self,index,customization):
        if 0<=index<len(self.items): self.items[index].customization=customization; return self.items[index]
    def get_subtotal(self): return sum(i.get_subtotal() for i in self.items)
    get_total=get_subtotal
    def get_item_count(self): return sum(i.quantity for i in self.items)
    def is_empty(self): return not self.items
    def clear(self): self.items.clear()
    def to_dict(self): return {"items":[i.to_dict() for i in self.items],"subtotal":self.get_subtotal(),"total":self.get_total()}
