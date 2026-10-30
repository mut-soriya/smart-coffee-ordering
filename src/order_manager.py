from datetime import datetime
from enum import Enum
import random

class OrderStatus(str,Enum): CART="CART"; PENDING="PENDING"; PREPARING="PREPARING"; READY="READY"; COMPLETED="COMPLETED"; CANCELLED="CANCELLED"
class Order:
    def __init__(self,cart):
        self.order_id=f"SC-{random.randint(100000,999999)}"; self.items=list(cart.items); self.subtotal=cart.get_subtotal(); self.total=cart.get_total(); self.status=OrderStatus.PENDING.value; self.created_at=datetime.now()
    def set_status(self,status): self.status=status.value if isinstance(status,OrderStatus) else status
    def to_dict(self): return {"order_id":self.order_id,"items":[i.to_dict() for i in self.items],"subtotal":self.subtotal,"total":self.total,"status":self.status,"created_at":self.created_at.isoformat()}

class OrderManager:
    def __init__(self): self.orders=[]
    def create_order(self,cart):
        if cart.is_empty(): raise ValueError("Cannot create an order from an empty cart.")
        o=Order(cart); self.orders.append(o); return o
    def get_order(self,oid): return next((o for o in self.orders if o.order_id==oid),None)
    def get_all_orders(self): return list(self.orders)
    def start_preparing(self,oid): return self._set(oid,OrderStatus.PREPARING)
    def mark_ready(self,oid): return self._set(oid,OrderStatus.READY)
    def complete_order(self,oid): return self._set(oid,OrderStatus.COMPLETED)
    def cancel_order(self,oid): return self._set(oid,OrderStatus.CANCELLED)
    def _set(self,oid,status):
        o=self.get_order(oid);
        if o: o.set_status(status)
        return o