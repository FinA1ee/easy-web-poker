from enum import Enum

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        
    def add_card(self, card):
        self.hand.append(card)
        
    def clear_hand(self):
        self.hand = [] 
    
    def set_position(self, position):
        self.position = position
        
    def get_position(self):
        return self.position