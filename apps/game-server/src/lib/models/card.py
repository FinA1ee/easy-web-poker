from enum import Enum
from typing import List

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        # Get rank display value (use 10 for 10, J for Jack, etc.)
        rank_display = {
            Rank.TEN: "10",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A"
        }.get(self.rank, str(self.rank.value))
        
        return f"{rank_display}{self.suit.value}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank.value < other.rank.value