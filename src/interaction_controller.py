from enum import Enum
import time

class InteractionState(str,Enum): IDLE="WELCOME"; HELP="HELP"; CATEGORY="CATEGORY"; PRODUCTS="PRODUCTS"; CUSTOMIZATION="CUSTOMIZATION"; CART="CART"; REVIEW="REVIEW"; CONFIRMED="CONFIRMED"; TICKET="TICKET"
class InteractionController:
    def __init__(self): self.state=InteractionState.IDLE; self.category_index=0; self.product_index=0; self.option_index=0; self.cart_index=0; self.last_pinch=0
    def reset(self): self.state=InteractionState.IDLE; self.category_index=0; self.product_index=0; self.option_index=0; self.cart_index=0; self.last_pinch=0
    def set_state(self,state): self.state=InteractionState(state)
    def handle_gesture(self,gesture):
        if gesture=="NONE": return None
        s=self.state
        if s==InteractionState.HELP and gesture=="PINCH": self.state=InteractionState.CATEGORY; return "OPEN_CATEGORIES"
        if s==InteractionState.CATEGORY:
            if gesture=="SWIPE_LEFT": return "PREVIOUS_CATEGORY"
            if gesture=="SWIPE_RIGHT": return "NEXT_CATEGORY"
            if gesture=="PINCH": return "SELECT_CATEGORY"
            if gesture=="FIST": self.state=InteractionState.IDLE; return "CANCEL"
        if s==InteractionState.PRODUCTS:
            if gesture=="SWIPE_LEFT": return "PREVIOUS_PRODUCT"
            if gesture=="SWIPE_RIGHT": return "NEXT_PRODUCT"
            if gesture=="PINCH": return "SELECT_PRODUCT"
            if gesture=="FIST": self.state=InteractionState.CATEGORY; return "BACK"
        if s==InteractionState.CUSTOMIZATION:
            if gesture=="SWIPE_LEFT": return "PREVIOUS_OPTION"
            if gesture=="SWIPE_RIGHT": return "NEXT_OPTION"
            if gesture=="SWIPE_UP": return "INCREASE_OPTION"
            if gesture=="SWIPE_DOWN": return "DECREASE_OPTION"
            if gesture=="PINCH": return "ADD_TO_CART"
            if gesture=="FIST": self.state=InteractionState.PRODUCTS; return "BACK"
        if s==InteractionState.CART:
            if gesture=="PINCH": return "PROCEED_TO_REVIEW"
            if gesture=="FIST": self.state=InteractionState.PRODUCTS; return "CONTINUE_ORDERING"
        if s==InteractionState.REVIEW:
            if gesture=="FIST": self.state=InteractionState.CART; return "BACK"
        return None
