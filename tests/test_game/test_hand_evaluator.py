import pytest
from web_poker.models.card import Card, Suit, Rank
from web_poker.game.hand_evaluator import HandEvaluator, HandRank

# Fixture for common card combinations
@pytest.fixture
def royal_flush():
    return [
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.HEARTS, Rank.KING),
        Card(Suit.HEARTS, Rank.QUEEN),
        Card(Suit.HEARTS, Rank.JACK),
        Card(Suit.HEARTS, Rank.TEN)
    ]

@pytest.fixture
def four_of_a_kind():
    return [
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.CLUBS, Rank.ACE),
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.HEARTS, Rank.KING)
    ]

@pytest.fixture
def two_pair():
    return [
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.CLUBS, Rank.KING),
        Card(Suit.SPADES, Rank.KING),
        Card(Suit.HEARTS, Rank.QUEEN)
    ]

class TestHandEvaluator:
    def test_evaluate_royal_flush(self, royal_flush):
        rank, cards = HandEvaluator.evaluate_hand(royal_flush)
        assert rank == HandRank.ROYAL_FLUSH
        assert len(cards) == 5

    def test_evaluate_four_of_a_kind(self, four_of_a_kind):
        rank, cards = HandEvaluator.evaluate_hand(four_of_a_kind)
        assert rank == HandRank.FOUR_OF_A_KIND
        assert len(cards) == 5
        # Check that we have all four aces
        aces = [card for card in cards if card.rank == Rank.ACE]
        assert len(aces) == 4
        # Check that king is the kicker
        assert cards[-1].rank == Rank.KING

    def test_evaluate_two_pair(self, two_pair):
        rank, cards = HandEvaluator.evaluate_hand(two_pair)
        assert rank == HandRank.TWO_PAIR
        assert len(cards) == 5

    def test_invalid_hand_size(self):
        invalid_hand = [Card(Suit.HEARTS, Rank.ACE)] * 4  # Only 4 cards
        with pytest.raises(ValueError):
            HandEvaluator.evaluate_hand(invalid_hand)

    def test_compare_hands_different_ranks(self, royal_flush, four_of_a_kind):
        # Royal flush should beat four of a kind
        result = HandEvaluator.compare_hands(royal_flush, four_of_a_kind)
        assert result == 1

        # Reverse comparison
        result = HandEvaluator.compare_hands(four_of_a_kind, royal_flush)
        assert result == -1

    def test_compare_hands_same_rank_different_values(self):
        # Two pairs: Aces and Kings vs Aces and Queens
        hand1 = [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN)
        ]
        
        hand2 = [
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.JACK)
        ]
        
        result = HandEvaluator.compare_hands(hand1, hand2)
        assert result == 1  # hand1 should win (higher second pair)

    def test_compare_hands_exact_tie(self):
        # Same cards, different suits
        hand1 = [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN)
        ]
        
        hand2 = [
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.QUEEN)
        ]
        
        result = HandEvaluator.compare_hands(hand1, hand2)
        assert result == 0  # Should be a tie

    def test_seven_card_hand(self):
        # Test with 7 cards (Texas Hold'em scenario)
        seven_cards = [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.DIAMONDS, Rank.TWO),
            Card(Suit.CLUBS, Rank.THREE)
        ]
        
        rank, cards = HandEvaluator.evaluate_hand(seven_cards)
        assert rank == HandRank.TWO_PAIR
        assert len(cards) == 5  # Should still return best 5 cards 