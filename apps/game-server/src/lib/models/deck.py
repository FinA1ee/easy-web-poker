from typing import List
import random
from .card import Card, Suit, Rank

class Deck:
    def __init__(self):
        """Initialize a new deck with 52 cards."""
        self.cards: List[Card] = self._create_deck()
        
    def _create_deck(self) -> List[Card]:
        """Create a standard 52-card deck."""
        return [Card(suit, rank) 
                for suit in Suit 
                for rank in Rank]
    
    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        """Draw a card from the top of the deck."""
        if not self.cards:
            raise ValueError("No cards left in deck")
        return self.cards.pop()
    
    def draw_multiple(self, count: int) -> List[Card]:
        """Draw multiple cards from the deck."""
        if count < 0:
            raise ValueError("Invalid count")
        if count > len(self.cards):
            raise ValueError(f"Not enough cards in deck. Requested: {count}, Available: {len(self.cards)}")
        return [self.draw() for _ in range(count)]
    
    def reset(self) -> None:
        """Reset the deck to its original state."""
        self.cards = self._create_deck()
        
    def __len__(self) -> int:
        """Return the number of cards remaining in the deck."""
        return len(self.cards) 