class KitchenQueue:
    def __init__(self,order_manager): self.order_manager=order_manager
    def get_pending(self): return [o for o in self.order_manager.orders if o.status=="PENDING"]
    def get_preparing(self): return [o for o in self.order_manager.orders if o.status=="PREPARING"]
    def get_ready(self): return [o for o in self.order_manager.orders if o.status=="READY"]
    def start_order(self,oid): return self.order_manager.start_preparing(oid)
    def mark_order_ready(self,oid): return self.order_manager.mark_ready(oid)
    def complete_order(self,oid): return self.order_manager.complete_order(oid)
    def get_queue_summary(self): return {"pending":len(self.get_pending()),"preparing":len(self.get_preparing()),"ready":len(self.get_ready())}
