import pytest
from web_poker.models.card import Card, Suit, Rank

class TestCard:
    """
    Test Strategy:
    1. Card Creation
    2. String Representation
    3. Card Comparisons
    4. Edge Cases
    """

    def test_card_creation(self):
        # Test basic card creation
        card = Card(Suit.HEARTS, Rank.ACE)
        assert card.suit == Suit.HEARTS
        assert card.rank == Rank.ACE

    def test_card_string_representation(self):
        # Test string formatting for different cards
        test_cases = [
            (Card(Suit.HEARTS, Rank.ACE), "A♥"),
            (Card(Suit.SPADES, Rank.KING), "K♠"),
            (Card(Suit.DIAMONDS, Rank.TEN), "10♦"),
            (Card(Suit.CLUBS, Rank.TWO), "2♣")
        ]
        
        for card, expected in test_cases:
            assert str(card) == expected

    def test_card_equality(self):
        # Test card equality comparisons
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.HEARTS, Rank.ACE)
        card3 = Card(Suit.SPADES, Rank.ACE)
        
        assert card1 == card2
        assert card1 != card3
        assert card1 != "not a card"

    def test_card_comparison(self):
        # Test card ranking comparisons
        ace = Card(Suit.HEARTS, Rank.ACE)
        king = Card(Suit.HEARTS, Rank.KING)
        queen = Card(Suit.HEARTS, Rank.QUEEN)
        
        assert king < ace
        assert queen < king
        assert not ace < king

    def test_card_sorting(self):
        # Test that cards can be properly sorted
        cards = [
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING)
        ]
        
        sorted_cards = sorted(cards)
        assert sorted_cards[-1].rank == Rank.ACE 