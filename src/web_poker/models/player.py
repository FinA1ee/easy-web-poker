class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        
    def add_card(self, card):
        self.hand.append(card)
        
    def clear_hand(self):
        self.hand = [] 