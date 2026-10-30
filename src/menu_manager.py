import json
from pathlib import Path
from .product import Product

class MenuManager:
    def __init__(self,menu_path="data/menu.json"):
        self.menu_path=Path(menu_path); self.products={}; self.categories=[]; self.load()
    def load(self):
        data=json.loads(self.menu_path.read_text(encoding="utf-8")); self.products={p["id"]:Product.from_dict({**{k:v for k,v in p.items() if k != "id"},"product_id":p["id"],"image":p.get("image","")}) for p in data["products"]}; self.categories=data.get("categories",[])
    def reload(self): self.load()
    def count_products(self): return len(self.products)
    def get_all_products(self): return list(self.products.values())
    def get_product(self,pid): return self.products.get(pid)
    def get_categories(self): return self.categories
    def get_category_names(self): return [c["name"] for c in self.categories]
    def get_category(self,cid): return next((c for c in self.categories if c["id"]==cid),None)
    def get_products_by_category(self,cid):
        c=self.get_category(cid); return [self.products[x] for x in c["products"] if x in self.products] if c else []
    def get_available_products_by_category(self,cid): return [p for p in self.get_products_by_category(cid) if p.available]
    def search_products(self,q): return [p for p in self.products.values() if q.lower() in p.name.lower()]
    def set_product_availability(self,pid,value):
        if pid in self.products: self.products[pid].available=value
