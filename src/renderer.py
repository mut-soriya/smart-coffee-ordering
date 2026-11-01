import math
import pygame
from .config import SCREEN_WIDTH,SCREEN_HEIGHT,FPS

ESP=(58,31,20); DEEP=(74,40,26); COF=(107,62,38); CAR=(168,102,53); GOLD=(201,139,74); CREAM=(247,235,221); LC=(255,248,240); BEIGE=(234,216,197); OK=(46,155,87); ERR=(201,75,69); WARN=(216,154,50); WHITE=(255,255,255); MUTED=(120,95,80)

class Renderer:
    WIDTH=SCREEN_WIDTH; HEIGHT=SCREEN_HEIGHT; FPS=FPS
    def __init__(self):
        pygame.init(); self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT)); pygame.display.set_caption("Smart Coffee Ordering — Touchless Kiosk"); self.clock=pygame.time.Clock(); self.current_screen="welcome"; self.cursor=(self.WIDTH//2,self.HEIGHT//2); self.cursor_visible=True; self.gesture="NONE"; self.toast_text=""; self.toast_until=0; self.fonts={s:pygame.font.SysFont("Arial",s,bold=False) for s in [14,16,18,20,22,24,28,32,36,44,54,64]}; self.bold={s:pygame.font.SysFont("Arial",s,bold=True) for s in [16,18,20,22,24,28,32,36,44,54,64]}
    def set_cursor_position(self,x,y): self.cursor=(int(x),int(y))
    def set_gesture(self,g): self.gesture=g
    def toast(self,text,seconds=1.3): self.toast_text=text; self.toast_until=pygame.time.get_ticks()/1000+seconds
    def _get_font(self, size, bold=False):
        """Return a cached font for any requested size."""
        size = max(1, int(size))
        cache = self.bold if bold else self.fonts
        if size not in cache:
            cache[size] = pygame.font.SysFont("Arial", size, bold=bold)
        return cache[size]

    def text(self, s, size, color=ESP, bold=False, center=False):
        """Render text without requiring the size to be pre-registered."""
        font = self._get_font(size, bold)
        surf = font.render(str(s), True, color)
        r = surf.get_rect()
        if center:
            r.center = (self.WIDTH // 2, self.HEIGHT // 2)
        return surf, r
    def rounded(self,rect,color,radius=24,border=None,width=1): pygame.draw.rect(self.screen,color,rect,border_radius=radius); border and pygame.draw.rect(self.screen,border,rect,width,border_radius=radius)
    def header(self,title,back=False,cart_count=0):
        pygame.draw.rect(self.screen,CREAM,(0,0,self.WIDTH,92));
        if back: self.button((38,22,120,52),"←  BACK",secondary=True,size=18)
        surf,_=self.text(title,30,ESP,True); self.screen.blit(surf,(self.WIDTH//2-surf.get_width()//2,27))
        self.status((1000,22,145,42)); self.button((1155,22,87,42),f"🛒 {cart_count}",secondary=False,size=16)
    def status(self,rect):
        x,y,w,h=rect; self.rounded(rect,WHITE,18,(225,210,195),1); col=OK if self.gesture!="NONE" else COF; pygame.draw.circle(self.screen,col,(x+15,y+h//2),5); label="HAND DETECTED" if self.gesture!="NONE" else "CAMERA READY"; surf,_=self.text(label,13,COF,True); self.screen.blit(surf,(x+26,y+13))
    def button(self,rect,label,secondary=False,hold=False,size=20,hover=False):
        color=(WHITE if secondary else CAR); border=COF if secondary else None; self.rounded(rect,color,18,border,1); surf,_=self.text(label,size,ESP if secondary or not hold else CREAM,True); self.screen.blit(surf,surf.get_rect(center=pygame.Rect(rect).center));
    def card(self,rect,selected=False,disabled=False):
        color=(248,248,248) if disabled else WHITE; border=GOLD if selected else (225,210,195); self.rounded(rect,color,26,border,3 if selected else 1)
    def coffee_icon(self,cx,cy,kind="coffee",scale=1.0):
        r=int(48*scale); pygame.draw.circle(self.screen,(245,226,202),(cx,cy),r); pygame.draw.ellipse(self.screen,(107,62,38),(cx-r*.55,cy-r*.15,cx+r*1.1,cy+r*.7)); pygame.draw.arc(self.screen,(107,62,38),(cx+r*.35,cy-r*.15,cx+r*1.0,cy+r*.6),-1.2,1.2,5); pygame.draw.arc(self.screen,(180,120,80),(cx-r*.3,cy-r*.75,cx+r*.3,cy-r*.05),2.8,6.0,3)
    def footer(self,msg):
        pygame.draw.rect(self.screen,(255,255,255),(0,664,self.WIDTH,56)); surf,_=self.text(msg,18,COF,False); self.screen.blit(surf,surf.get_rect(center=(self.WIDTH//2,692)))
    def render(self,app=None):
        self.screen.fill(CREAM)
        if self.current_screen=="welcome": self.welcome()
        elif self.current_screen=="help": self.help()
        elif self.current_screen=="categories": self.categories(app)
        elif self.current_screen=="products": self.products(app)
        elif self.current_screen=="customization": self.customization(app)
        elif self.current_screen=="cart": self.cart(app)
        elif self.current_screen=="review": self.review(app)
        elif self.current_screen=="confirmed": self.confirmed(app)
        elif self.current_screen=="ticket": self.ticket(app)
        elif self.current_screen=="kitchen": self.kitchen(app)
        elif self.current_screen=="camera_error": self.error("CAMERA UNAVAILABLE","Please check your webcam.","TRY AGAIN",ERR)
        elif self.current_screen=="hand_error": self.error("SHOW YOUR HAND","Place your hand inside the interaction area.","RETRY",WARN)
        elif self.current_screen=="gesture_error": self.error("GESTURE NOT RECOGNIZED","Try again and keep your hand steady.","RETRY",WARN)
        elif self.current_screen=="timeout": self.timeout()
        self.draw_cursor(); self.draw_toast()
    def welcome(self):
        self.screen.fill(CREAM); self.coffee_icon(220,250,"coffee",2.0);
        surf,_=self.text("☕ SMART",54,ESP,True); self.screen.blit(surf,(520,125)); surf,_=self.text("COFFEE",54,ESP,True); self.screen.blit(surf,(520,190)); surf,_=self.text("ORDERING",54,ESP,True); self.screen.blit(surf,(520,255)); surf,_=self.text("Touchless Ordering with Hand Gestures",22,COF); self.screen.blit(surf,(522,325)); self.button((520,385,280,70),"START ORDER",False,size=22); self.button((820,385,190,70),"?  HOW TO ORDER",True,size=18); surf,_=self.text("Point with one index finger to move; hold to select",18,COF); self.screen.blit(surf,(520,485)); self.status((520,535,150,40)); surf,_=self.text("Camera is used locally for hand gesture control.",14,MUTED); self.screen.blit(surf,(690,547)); self.footer("☝️ Point / move • ☝️ Hold / select • ✌️ Two fingers / scroll • 🤏 Pinch / grab • ✊ Fist / back")
    def help(self):
        self.header("HOW TO ORDER",True); labels=[("☝️","Point","MOVE"),("☝️","Hold","SELECT"),("✌️","Two fingers","SCROLL"),("🤏","Pinch","GRAB"),("✊","Fist","BACK")];
        for i,(ic,n,sub) in enumerate(labels):
            x=55+(i%4)*300; y=120+(i//4)*220; self.card((x,y,275,185)); surf,_=self.text(ic,44,CAR,True); self.screen.blit(surf,surf.get_rect(center=(x+137,y+55))); surf,_=self.text(n,21,ESP,True); self.screen.blit(surf,surf.get_rect(center=(x+137,y+105))); surf,_=self.text(sub,14,COF,True); self.screen.blit(surf,surf.get_rect(center=(x+137,y+140)));
        self.button((520,570,240,62),"GOT IT",False,size=20); self.footer("Point to move • Hold to select • Two fingers to scroll • Pinch to grab • Fist to go back")
    def categories(self,app):
        self.header("WHAT WOULD YOU LIKE?",True,app.cart.get_item_count()); cats=app.menu_manager.get_categories();
        for i,c in enumerate(cats):
            x=110+(i%2)*540; y=125+(i//2)*230; self.card((x,y,500,190),selected=(i==app.category_index)); self.coffee_icon(x+100,y+95,scale=.85); surf,_=self.text(c['name'],28,ESP,True); self.screen.blit(surf,(x+175,y+65)); n=len(app.menu_manager.get_products_by_category(c['id'])); surf,_=self.text(f"{n} products",16,COF); self.screen.blit(surf,(x+175,y+108));
        self.footer("☝️ Point / move • Hold / select • ✌️ Two fingers / scroll • 🤏 Pinch / grab • ✊ Fist / back")
    def products(self,app):
        cat=app.menu_manager.get_categories()[app.category_index]; products=app.menu_manager.get_products_by_category(cat['id']); self.header(cat['name'],True,app.cart.get_item_count());
        for i,p in enumerate(products[:4]):
            x=50+i*300; y=125; self.card((x,y,275,450),selected=(i==app.product_index),disabled=not p.available); self.coffee_icon(x+137,y+95,scale=.9); surf,_=self.text(p.name,23,ESP,True); self.screen.blit(surf,surf.get_rect(center=(x+137,y+180)));
            desc=p.description[:27]+('…' if len(p.description)>27 else ''); surf,_=self.text(desc,14,COF); self.screen.blit(surf,surf.get_rect(center=(x+137,y+220))); surf,_=self.text(f"${p.price:.2f}",27,CAR,True); self.screen.blit(surf,surf.get_rect(center=(x+137,y+270))); self.rounded((x+75,y+315,125,34), (214,239,224) if p.available else (225,225,225),17); surf,_=self.text("AVAILABLE" if p.available else "UNAVAILABLE",12,OK if p.available else MUTED,True); self.screen.blit(surf,surf.get_rect(center=(x+137,y+332)));
        self.footer("☝️ Point / move • Hold / select • ✌️ Two fingers / scroll • 🤏 Pinch / grab • ✊ Fist / back")
    def customization(self,app):
        p=app.selected_product; self.header(p.name,True,app.cart.get_item_count()); self.coffee_icon(250,285,scale=1.8); surf,_=self.text(p.name,34,ESP,True); self.screen.blit(surf,(500,118)); surf,_=self.text(f"${p.price:.2f}",25,CAR,True); self.screen.blit(surf,(500,160)); y=210
        groups=[("SIZE",p.sizes,app.custom["size"]),("TEMPERATURE",p.temperatures,app.custom["temperature"]),("SUGAR",p.sugar_levels,app.custom["sugar"]),("MILK",p.milk_options,app.custom["milk"]),("ADD-ONS",p.toppings,app.custom["toppings"])];
        for title,opts,selected in groups:
            if not opts: continue
            surf,_=self.text(title,14,COF,True); self.screen.blit(surf,(500,y)); xx=500
            for o in opts:
                w=max(82, len(o)*11+24); on=(o in selected if isinstance(selected,list) else o==selected); self.rounded((xx,y+25,w,38),ESP if on else WHITE,12,None); surf,_=self.text(o,13,CREAM if on else ESP,True); self.screen.blit(surf,surf.get_rect(center=(xx+w/2,y+44))); xx+=w+8
            y+=70
        total=p.price+app.custom.get('extra_price',0); surf,_=self.text(f"TOTAL  ${total*app.custom['quantity']:.2f}",30,CAR,True); self.screen.blit(surf,(500,570)); self.button((865,550,280,62),"ADD TO CART",False,size=20); self.footer("☝️ Hold to select • ✌️ Two fingers to scroll • 🤏 Pinch to grab • ✊ Fist to back")
    def cart(self,app):
        self.header("YOUR CART",True,app.cart.get_item_count());
        if app.cart.is_empty():
            surf,_=self.text("🛒",70,CAR,True); self.screen.blit(surf,surf.get_rect(center=(300,280))); surf,_=self.text("YOUR CART IS EMPTY",32,ESP,True); self.screen.blit(surf,(390,235)); surf,_=self.text("Add a coffee to get started.",18,COF); self.screen.blit(surf,(390,285)); self.button((390,340,230,60),"BROWSE MENU",False,size=18); self.footer("Pinch BROWSE MENU to continue"); return
        y=125
        for i,item in enumerate(app.cart.items):
            self.card((55,y,760,130)); self.coffee_icon(125,y+65,scale=.55); surf,_=self.text(item.product.name,22,ESP,True); self.screen.blit(surf,(190,y+25)); summary=" • ".join(str(v) for k,v in item.customization.items() if k in ['size','temperature','sugar','milk'] and v); surf,_=self.text(summary[:48],14,COF); self.screen.blit(surf,(190,y+60)); self.button((580,y+78,75,36),"−",True,size=20); surf,_=self.text(str(item.quantity),20,ESP,True); self.screen.blit(surf,(670,y+84)); self.button((700,y+78,75,36),"+",True,size=20); surf,_=self.text(f"${item.get_subtotal():.2f}",22,CAR,True); self.screen.blit(surf,(820,y+35)); self.button((820,y+76,75,34),"EDIT",True,size=12); y+=145
        self.card((900,125,325,360)); surf,_=self.text("ORDER SUMMARY",22,ESP,True); self.screen.blit(surf,(935,155)); surf,_=self.text(f"SUBTOTAL   ${app.cart.get_subtotal():.2f}",18,COF); self.screen.blit(surf,(935,215)); surf,_=self.text(f"TOTAL   ${app.cart.get_total():.2f}",32,ESP,True); self.screen.blit(surf,(935,265)); self.button((935,340,255,58),"CONTINUE ORDERING",True,size=15); self.button((935,415,255,65),"HOLD TO CONFIRM",False,hold=True,size=17); self.footer("☝️ Hold to select • ✊ Fist to go back")
    def review(self,app):
        self.header("REVIEW YOUR ORDER",True,app.cart.get_item_count()); y=120
        for item in app.cart.items:
            self.card((110,y,1060,90)); surf,_=self.text(f"{item.product.name} × {item.quantity}",21,ESP,True); self.screen.blit(surf,(145,y+18)); summary=" • ".join(str(v) for k,v in item.customization.items() if k in ['size','temperature','sugar','milk'] and v); surf,_=self.text(summary,14,COF); self.screen.blit(surf,(145,y+52)); surf,_=self.text(f"${item.get_subtotal():.2f}",21,CAR,True); self.screen.blit(surf,(990,y+32)); y+=105
        surf,_=self.text(f"TOTAL  ${app.cart.get_total():.2f}",34,ESP,True); self.screen.blit(surf,(760,535)); self.button((190,520,300,62),"EDIT ORDER",True,size=19); self.button((500,520,300,62),"HOLD TO CONFIRM",False,hold=True,size=19); self.footer("☝️ Hold to select • ✊ Fist to go back")
    def confirmed(self,app):
        self.screen.fill(CREAM); pygame.draw.circle(self.screen,OK,(240,300),95); surf,_=self.text("✓",90,WHITE,True); self.screen.blit(surf,surf.get_rect(center=(240,300))); surf,_=self.text("ORDER CONFIRMED!",40,OK,True); self.screen.blit(surf,(400,175)); surf,_=self.text("Your order has been received.",20,COF); self.screen.blit(surf,(402,230)); oid=app.last_order.order_id if app.last_order else "SC-000000"; surf,_=self.text(oid,54,ESP,True); self.screen.blit(surf,(400,290)); surf,_=self.text(f"Total  ${app.last_order.total:.2f}" if app.last_order else "Total  $0.00",25,CAR,True); self.screen.blit(surf,(402,365)); self.button((400,440,260,58),"VIEW TICKET",True,size=18); self.button((680,440,220,58),"NEW ORDER",False,size=18); self.footer("Your order is being prepared • Show your order number at pickup")
    def ticket(self,app):
        self.header("ORDER TICKET",False); r=pygame.Rect(360,110,560,520); self.rounded(r,WHITE,4); surf,_=self.text("SMART COFFEE",26,ESP,True); self.screen.blit(surf,surf.get_rect(center=(640,150))); surf,_=self.text(app.last_order.order_id if app.last_order else "SC-000000",40,ESP,True); self.screen.blit(surf,surf.get_rect(center=(640,205))); pygame.draw.line(self.screen,BEIGE,(400,240),(880,240),2); y=275
        if app.last_order:
            for item in app.last_order.items:
                surf,_=self.text(f"{item.product.name} × {item.quantity}",18,ESP,True); self.screen.blit(surf,(410,y)); surf,_=self.text(f"${item.get_subtotal():.2f}",18,CAR,True); self.screen.blit(surf,(790,y)); y+=45
            surf,_=self.text(f"TOTAL  ${app.last_order.total:.2f}",28,ESP,True); self.screen.blit(surf,(410,y+20));
        self.button((500,585,280,54),"NEW ORDER",False,size=18); self.footer("Please remember your order number")
    def kitchen(self,app):
        self.header("KITCHEN QUEUE"); cols=[("PENDING",app.kitchen.get_pending()),("PREPARING",app.kitchen.get_preparing()),("READY",app.kitchen.get_ready())];
        for ci,(title,orders) in enumerate(cols):
            x=30+ci*415; self.card((x,115,390,500)); surf,_=self.text(title,22,ESP,True); self.screen.blit(surf,(x+20,140)); yy=185
            for o in orders:
                self.card((x+18,yy,354,115)); surf,_=self.text(o.order_id,18,ESP,True); self.screen.blit(surf,(x+35,yy+15)); surf,_=self.text(", ".join(f"{i.product.name} × {i.quantity}" for i in o.items),14,COF); self.screen.blit(surf,(x+35,yy+45)); surf,_=self.text(f"${o.total:.2f}",18,CAR,True); self.screen.blit(surf,(x+270,yy+15)); yy+=130
        self.footer("Staff view • Pending → Preparing → Ready")
    def error(self,title,msg,button,color):
        self.screen.fill(CREAM); self.rounded((230,150,820,420),WHITE,32); pygame.draw.circle(self.screen,color,(640,250),55); surf,_=self.text("!",54,WHITE,True); self.screen.blit(surf,surf.get_rect(center=(640,250))); surf,_=self.text(title,34,ESP,True); self.screen.blit(surf,surf.get_rect(center=(640,340))); surf,_=self.text(msg,18,COF); self.screen.blit(surf,surf.get_rect(center=(640,385))); self.button((520,440,240,60),button,False,size=18); self.footer("System status requires attention")
    def timeout(self):
        self.screen.fill(CREAM); self.rounded((280,160,720,380),WHITE,32); surf,_=self.text("ARE YOU STILL THERE?",32,ESP,True); self.screen.blit(surf,surf.get_rect(center=(640,235))); surf,_=self.text("No activity detected.",18,COF); self.screen.blit(surf,surf.get_rect(center=(640,285))); self.button((430,350,200,58),"CONTINUE",False,size=18); self.button((650,350,200,58),"RESET",True,size=18); self.footer("The session will reset automatically if no action is taken")
    def draw_cursor(self):
        if not self.cursor_visible: return
        x,y=self.cursor; pygame.draw.circle(self.screen,(201,139,74),(x,y),25,4); pygame.draw.circle(self.screen,ESP,(x,y),6);
        if self.gesture=="PINCH": pygame.draw.circle(self.screen,CAR,(x,y),13,3)
    def draw_toast(self):
        if self.toast_text and pygame.time.get_ticks()/1000<self.toast_until:
            surf,_=self.text(self.toast_text,18,CREAM,True); rect=pygame.Rect(0,0,surf.get_width()+50,52); rect.center=(640,105); self.rounded(rect,ESP,26,GOLD,2); self.screen.blit(surf,surf.get_rect(center=rect.center))
    def close(self): pygame.quit()
