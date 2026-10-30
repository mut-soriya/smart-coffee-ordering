class Product:
    def __init__(self, product_id, name, category, price, image="", available=True, description="", sizes=None, temperatures=None, sugar_levels=None, milk_options=None, toppings=None, image_url=None, **kwargs):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = float(price)
        self.image = image or image_url or ""
        self.image_url = image_url or image or ""
        self.available = available
        self.description = description
        self.sizes = sizes or []
        self.temperatures = temperatures or []
        self.sugar_levels = sugar_levels or []
        self.milk_options = milk_options or []
        self.toppings = toppings or []
    def get_price(self): return self.price
    def is_available(self): return self.available
    def set_available(self,value): self.available=bool(value)
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,d): return cls(**d)