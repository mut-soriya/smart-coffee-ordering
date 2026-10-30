const products = [
  {
    "id": "espresso",
    "name": "Espresso",
    "category": "hot",
    "price": 2.5,
    "image": "assets/coffee/espresso.jpg",
    "imageUrl": "https://images.pexels.com/photos/4736078/pexels-photo-4736078.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Rich and bold espresso with a smooth finish."
  },
  {
    "id": "double-espresso",
    "name": "Double Espresso",
    "category": "hot",
    "price": 3.25,
    "image": "assets/coffee/double-espresso.jpg",
    "imageUrl": "https://images.pexels.com/photos/8736396/pexels-photo-8736396.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "A stronger double shot of smooth espresso."
  },
  {
    "id": "americano",
    "name": "Americano",
    "category": "hot",
    "price": 2.75,
    "image": "assets/coffee/americano.jpg",
    "imageUrl": "https://images.pexels.com/photos/11234324/pexels-photo-11234324.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Espresso balanced with hot water."
  },
  {
    "id": "long-black",
    "name": "Long Black",
    "category": "hot",
    "price": 2.75,
    "image": "assets/coffee/long-black.jpg",
    "imageUrl": "https://images.pexels.com/photos/29497982/pexels-photo-29497982.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Bold espresso poured over hot water."
  },
  {
    "id": "cappuccino",
    "name": "Cappuccino",
    "category": "hot",
    "price": 3.5,
    "image": "assets/coffee/cappuccino.jpg",
    "imageUrl": "https://images.pexels.com/photos/5112652/pexels-photo-5112652.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Espresso with steamed milk and creamy foam."
  },
  {
    "id": "latte",
    "name": "Latte",
    "category": "hot",
    "price": 3.5,
    "image": "assets/coffee/latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/5419239/pexels-photo-5419239.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Smooth espresso blended with steamed milk."
  },
  {
    "id": "vanilla-latte",
    "name": "Vanilla Latte",
    "category": "hot",
    "price": 4,
    "image": "assets/coffee/vanilla-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/18395616/pexels-photo-18395616.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Creamy latte with sweet vanilla flavor."
  },
  {
    "id": "caramel-latte",
    "name": "Caramel Latte",
    "category": "hot",
    "price": 4,
    "image": "assets/coffee/caramel-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/11277040/pexels-photo-11277040.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Smooth latte with rich caramel flavor."
  },
  {
    "id": "hazelnut-latte",
    "name": "Hazelnut Latte",
    "category": "hot",
    "price": 4,
    "image": "assets/coffee/hazelnut-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/35852545/pexels-photo-35852545.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Creamy latte with roasted hazelnut notes."
  },
  {
    "id": "mocha",
    "name": "Mocha",
    "category": "hot",
    "price": 4.25,
    "image": "assets/coffee/mocha.jpg",
    "imageUrl": "https://images.pexels.com/photos/8004561/pexels-photo-8004561.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Espresso, chocolate and steamed milk."
  },
  {
    "id": "white-mocha",
    "name": "White Mocha",
    "category": "hot",
    "price": 4.25,
    "image": "assets/coffee/white-mocha.jpg",
    "imageUrl": "https://images.pexels.com/photos/5946979/pexels-photo-5946979.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Creamy espresso with white chocolate."
  },
  {
    "id": "caramel-macchiato",
    "name": "Caramel Macchiato",
    "category": "hot",
    "price": 4.5,
    "image": "assets/coffee/caramel-macchiato.jpg",
    "imageUrl": "https://images.pexels.com/photos/8004569/pexels-photo-8004569.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Espresso, milk and caramel drizzle."
  },
  {
    "id": "flat-white",
    "name": "Flat White",
    "category": "hot",
    "price": 3.75,
    "image": "assets/coffee/flat-white.jpg",
    "imageUrl": "https://images.pexels.com/photos/35079943/pexels-photo-35079943.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Velvety microfoam over rich espresso."
  },
  {
    "id": "cortado",
    "name": "Cortado",
    "category": "hot",
    "price": 3.5,
    "image": "assets/coffee/cortado.jpg",
    "imageUrl": "https://images.pexels.com/photos/32599385/pexels-photo-32599385.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Equal parts espresso and warm milk."
  },
  {
    "id": "macchiato",
    "name": "Macchiato",
    "category": "hot",
    "price": 3,
    "image": "assets/coffee/macchiato.jpg",
    "imageUrl": "https://images.pexels.com/photos/37745284/pexels-photo-37745284.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Espresso marked with a touch of foam."
  },
  {
    "id": "affogato",
    "name": "Affogato",
    "category": "hot",
    "price": 4.5,
    "image": "assets/coffee/affogato.jpg",
    "imageUrl": "https://images.pexels.com/photos/28729996/pexels-photo-28729996.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Espresso served over creamy vanilla ice cream."
  },
  {
    "id": "cinnamon-latte",
    "name": "Cinnamon Latte",
    "category": "hot",
    "price": 4,
    "image": "assets/coffee/cinnamon-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/32599371/pexels-photo-32599371.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Warm cinnamon blended into a creamy latte."
  },
  {
    "id": "honey-latte",
    "name": "Honey Latte",
    "category": "hot",
    "price": 4,
    "image": "assets/coffee/honey-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/33493391/pexels-photo-33493391.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Naturally sweet honey and smooth espresso."
  },
  {
    "id": "coconut-latte",
    "name": "Coconut Latte",
    "category": "hot",
    "price": 4.25,
    "image": "assets/coffee/coconut-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/8004564/pexels-photo-8004564.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Espresso with creamy coconut milk."
  },
  {
    "id": "cream-latte",
    "name": "Cream Latte",
    "category": "hot",
    "price": 4.25,
    "image": "assets/coffee/cream-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/12201275/pexels-photo-12201275.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Silky latte with a creamy finish."
  },
  {
    "id": "iced-americano",
    "name": "Iced Americano",
    "category": "iced",
    "price": 3,
    "image": "assets/coffee/iced-americano.jpg",
    "imageUrl": "https://images.pexels.com/photos/34046801/pexels-photo-34046801.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Chilled espresso with cold water and ice."
  },
  {
    "id": "iced-latte",
    "name": "Iced Latte",
    "category": "iced",
    "price": 3.75,
    "image": "assets/coffee/iced-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/20205946/pexels-photo-20205946.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Cold espresso and creamy milk over ice."
  },
  {
    "id": "iced-vanilla-latte",
    "name": "Iced Vanilla Latte",
    "category": "iced",
    "price": 4.25,
    "image": "assets/coffee/iced-vanilla-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/26238864/pexels-photo-26238864.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Vanilla latte served chilled over ice."
  },
  {
    "id": "iced-caramel-latte",
    "name": "Iced Caramel Latte",
    "category": "iced",
    "price": 4.25,
    "image": "assets/coffee/iced-caramel-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/5741238/pexels-photo-5741238.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Caramel latte served cold and refreshing."
  },
  {
    "id": "iced-hazelnut-latte",
    "name": "Iced Hazelnut Latte",
    "category": "iced",
    "price": 4.25,
    "image": "assets/coffee/iced-hazelnut-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/22221934/pexels-photo-22221934.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Hazelnut latte served chilled."
  },
  {
    "id": "iced-mocha",
    "name": "Iced Mocha",
    "category": "iced",
    "price": 4.5,
    "image": "assets/coffee/iced-mocha.jpg",
    "imageUrl": "https://images.pexels.com/photos/8284685/pexels-photo-8284685.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Chocolate espresso drink served over ice."
  },
  {
    "id": "iced-white-mocha",
    "name": "Iced White Mocha",
    "category": "iced",
    "price": 4.5,
    "image": "assets/coffee/iced-white-mocha.jpg",
    "imageUrl": "https://images.pexels.com/photos/4051583/pexels-photo-4051583.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "White chocolate espresso drink over ice."
  },
  {
    "id": "iced-caramel-macchiato",
    "name": "Iced Caramel Macchiato",
    "category": "iced",
    "price": 4.75,
    "image": "assets/coffee/iced-caramel-macchiato.jpg",
    "imageUrl": "https://images.pexels.com/photos/7935281/pexels-photo-7935281.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Iced espresso with milk and caramel."
  },
  {
    "id": "cold-brew",
    "name": "Cold Brew",
    "category": "iced",
    "price": 4,
    "image": "assets/coffee/cold-brew.jpg",
    "imageUrl": "https://images.pexels.com/photos/28056044/pexels-photo-28056044.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Slow-steeped coffee with a smooth finish."
  },
  {
    "id": "vanilla-cold-brew",
    "name": "Vanilla Cold Brew",
    "category": "iced",
    "price": 4.5,
    "image": "assets/coffee/vanilla-cold-brew.jpg",
    "imageUrl": "https://images.pexels.com/photos/13054437/pexels-photo-13054437.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Smooth cold brew with vanilla."
  },
  {
    "id": "caramel-cold-brew",
    "name": "Caramel Cold Brew",
    "category": "iced",
    "price": 4.5,
    "image": "assets/coffee/caramel-cold-brew.jpg",
    "imageUrl": "https://images.pexels.com/photos/14941250/pexels-photo-14941250.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Cold brew finished with caramel."
  },
  {
    "id": "nitro-cold-brew",
    "name": "Nitro Cold Brew",
    "category": "iced",
    "price": 4.75,
    "image": "assets/coffee/nitro-cold-brew.jpg",
    "imageUrl": "https://images.pexels.com/photos/10225266/pexels-photo-10225266.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Silky cold brew with a creamy texture."
  },
  {
    "id": "iced-espresso",
    "name": "Iced Espresso",
    "category": "iced",
    "price": 3.25,
    "image": "assets/coffee/iced-espresso.jpg",
    "imageUrl": "https://images.pexels.com/photos/13425585/pexels-photo-13425585.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Chilled espresso over ice."
  },
  {
    "id": "iced-flat-white",
    "name": "Iced Flat White",
    "category": "iced",
    "price": 4,
    "image": "assets/coffee/iced-flat-white.jpg",
    "imageUrl": "https://images.pexels.com/photos/20009435/pexels-photo-20009435.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Velvety espresso and milk served cold."
  },
  {
    "id": "dirty-latte",
    "name": "Dirty Latte",
    "category": "iced",
    "price": 4.25,
    "image": "assets/coffee/dirty-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/36457298/pexels-photo-36457298.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Chilled milk with a bold espresso shot."
  },
  {
    "id": "matcha-latte",
    "name": "Matcha Latte",
    "category": "non",
    "price": 4,
    "image": "assets/coffee/matcha-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/3650437/pexels-photo-3650437.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Creamy green tea latte with a smooth finish."
  },
  {
    "id": "iced-matcha-latte",
    "name": "Iced Matcha Latte",
    "category": "non",
    "price": 4.25,
    "image": "assets/coffee/iced-matcha-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/36522228/pexels-photo-36522228.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Refreshing matcha and milk over ice."
  },
  {
    "id": "chocolate-milk",
    "name": "Chocolate Milk",
    "category": "non",
    "price": 3.25,
    "image": "assets/coffee/chocolate-milk.jpg",
    "imageUrl": "https://images.pexels.com/photos/3776531/pexels-photo-3776531.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Creamy chocolate milk served chilled."
  },
  {
    "id": "iced-chocolate",
    "name": "Iced Chocolate",
    "category": "non",
    "price": 3.75,
    "image": "assets/coffee/iced-chocolate.jpg",
    "imageUrl": "https://images.pexels.com/photos/4828331/pexels-photo-4828331.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Rich chocolate drink served cold."
  },
  {
    "id": "hot-chocolate",
    "name": "Hot Chocolate",
    "category": "non",
    "price": 3.75,
    "image": "assets/coffee/hot-chocolate.jpg",
    "imageUrl": "https://images.pexels.com/photos/31609729/pexels-photo-31609729.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Warm and creamy classic hot chocolate."
  },
  {
    "id": "strawberry-milk",
    "name": "Strawberry Milk",
    "category": "non",
    "price": 3.75,
    "image": "assets/coffee/strawberry-milk.jpg",
    "imageUrl": "https://images.pexels.com/photos/19955847/pexels-photo-19955847.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Creamy milk with sweet strawberry flavor."
  },
  {
    "id": "strawberry-matcha",
    "name": "Strawberry Matcha",
    "category": "non",
    "price": 4.5,
    "image": "assets/coffee/strawberry-matcha.jpg",
    "imageUrl": "https://images.pexels.com/photos/4051560/pexels-photo-4051560.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Layered strawberry and creamy matcha."
  },
  {
    "id": "mango-matcha",
    "name": "Mango Matcha",
    "category": "non",
    "price": 4.5,
    "image": "assets/coffee/mango-matcha.jpg",
    "imageUrl": "https://images.pexels.com/photos/10530447/pexels-photo-10530447.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Tropical mango paired with smooth matcha."
  },
  {
    "id": "chai-latte",
    "name": "Chai Latte",
    "category": "non",
    "price": 4,
    "image": "assets/coffee/chai-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/15086188/pexels-photo-15086188.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Warm spiced chai blended with creamy milk."
  },
  {
    "id": "iced-chai-latte",
    "name": "Iced Chai Latte",
    "category": "non",
    "price": 4.25,
    "image": "assets/coffee/iced-chai-latte.jpg",
    "imageUrl": "https://images.pexels.com/photos/15086186/pexels-photo-15086186.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Chilled spiced chai with creamy milk."
  },
  {
    "id": "croissant",
    "name": "Croissant",
    "category": "bakery",
    "price": 2.75,
    "image": "assets/coffee/croissant.jpg",
    "imageUrl": "https://images.pexels.com/photos/37014532/pexels-photo-37014532.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Buttery, flaky classic French-style pastry."
  },
  {
    "id": "chocolate-croissant",
    "name": "Chocolate Croissant",
    "category": "bakery",
    "price": 3.25,
    "image": "assets/coffee/chocolate-croissant.jpg",
    "imageUrl": "https://images.pexels.com/photos/36667988/pexels-photo-36667988.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Flaky pastry filled with rich chocolate."
  },
  {
    "id": "blueberry-muffin",
    "name": "Blueberry Muffin",
    "category": "bakery",
    "price": 3,
    "image": "assets/coffee/blueberry-muffin.jpg",
    "imageUrl": "https://images.pexels.com/photos/28730007/pexels-photo-28730007.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Soft muffin packed with blueberries."
  },
  {
    "id": "chocolate-muffin",
    "name": "Chocolate Muffin",
    "category": "bakery",
    "price": 3,
    "image": "assets/coffee/chocolate-muffin.jpg",
    "imageUrl": "https://images.pexels.com/photos/35745300/pexels-photo-35745300.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Moist chocolate muffin with rich cocoa flavor."
  },
  {
    "id": "cheesecake",
    "name": "Cheesecake",
    "category": "bakery",
    "price": 4.5,
    "image": "assets/coffee/cheesecake.jpg",
    "imageUrl": "https://images.pexels.com/photos/37029476/pexels-photo-37029476.jpeg?auto=compress&cs=tinysrgb&w=1000",
    "description": "Creamy cheesecake with a smooth biscuit base."
  }
];
