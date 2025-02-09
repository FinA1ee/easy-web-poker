import pytest
from web_poker.models.deck import Deck
from web_poker.models.card import Card, Suit, Rank

class TestDeck:
    """
    Test Strategy:
    1. Deck Creation and Properties
    2. Card Drawing Operations
    3. Deck Manipulation (shuffle, reset)
    4. Error Cases
    5. Edge Cases
    """

    def test_deck_creation(self):
        # Test initial deck state
        deck = Deck()
        assert len(deck) == 52
        
        # Test all cards are unique
        card_strings = [str(card) for card in deck.cards]
        assert len(set(card_strings)) == 52

    def test_draw_single_card(self):
        deck = Deck()
        initial_size = len(deck)
        
        # Test single card draw
        card = deck.draw()
        assert isinstance(card, Card)
        assert len(deck) == initial_size - 1

    def test_draw_multiple_cards(self):
        deck = Deck()
        
        # Test drawing multiple cards
        cards = deck.draw_multiple(5)
        assert len(cards) == 5
        assert len(deck) == 47
        assert all(isinstance(card, Card) for card in cards)

    def test_shuffle(self):
        # Test that shuffle changes card order
        deck1 = Deck()
        deck2 = Deck()
        
        initial_order = [str(card) for card in deck1.cards.copy()]
        deck2.shuffle()
        shuffled_order = [str(card) for card in deck2.cards]
        
        # Check orders are different (very small chance they're the same)
        assert initial_order != shuffled_order
        # Check no cards were lost
        assert len(deck2) == 52

    def test_reset(self):
        deck = Deck()
        # Draw some cards and verify reset
        deck.draw_multiple(10)
        assert len(deck) == 42
        
        deck.reset()
        assert len(deck) == 52

    def test_empty_deck_error(self):
        deck = Deck()
        # Draw all cards
        deck.draw_multiple(52)
        
        # Verify error on empty deck
        with pytest.raises(ValueError, match="No cards left in deck"):
            deck.draw()

    def test_draw_too_many_cards_error(self):
        deck = Deck()
        
        # Try to draw more cards than available
        with pytest.raises(ValueError, match="Not enough cards"):
            deck.draw_multiple(53)

    def test_draw_negative_cards_error(self):
        deck = Deck()
        
        # Try to draw negative number of cards
        with pytest.raises(ValueError, match="Invalid count"):
            deck.draw_multiple(-1) 