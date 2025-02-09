from enum import Enum
from web_poker.models.card import Card, Rank
from typing import List, Tuple, Optional
from itertools import combinations
from collections import Counter

class HandRank(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

class HandEvaluator:
    @staticmethod
    def evaluate_hand(cards: List[Card]) -> Tuple[HandRank, List[Card]]:
        """
        Evaluates a poker hand and returns (rank, relevant_cards).
        Cards must be a list of 5-7 cards.
        """
        if not 5 <= len(cards) <= 7:
            raise ValueError("Hand must contain 5-7 cards")

        # Sort cards by rank (highest first)
        sorted_cards = sorted(cards, key=lambda x: x.rank.value, reverse=True)
        
        # Get all possible 5-card combinations if more than 5 cards
        five_card_combinations = combinations(sorted_cards, 5)
        best_hand = None
        best_rank = None
        
        for five_cards in five_card_combinations:
            # Check from highest rank to lowest
            # Royal Flush
            if HandEvaluator._is_royal_flush(five_cards):
                return HandRank.ROYAL_FLUSH, list(five_cards)
            
            # Straight Flush
            if HandEvaluator._is_straight_flush(five_cards):
                if not best_rank or best_rank.value < HandRank.STRAIGHT_FLUSH.value:
                    best_hand = five_cards
                    best_rank = HandRank.STRAIGHT_FLUSH
                
            # Four of a Kind
            four_kind = HandEvaluator._is_four_of_kind(five_cards)
            if four_kind:
                if not best_rank or best_rank.value < HandRank.FOUR_OF_A_KIND.value:
                    best_hand = four_kind
                    best_rank = HandRank.FOUR_OF_A_KIND
                
            # Full House
            full_house = HandEvaluator._is_full_house(five_cards)
            if full_house:
                if not best_rank or best_rank.value < HandRank.FULL_HOUSE.value:
                    best_hand = full_house
                    best_rank = HandRank.FULL_HOUSE
                
            # Flush
            if HandEvaluator._is_flush(five_cards):
                if not best_rank or best_rank.value < HandRank.FLUSH.value:
                    best_hand = five_cards
                    best_rank = HandRank.FLUSH
            
            # Straight
            if HandEvaluator._is_straight(five_cards):
                if not best_rank or best_rank.value < HandRank.STRAIGHT.value:
                    best_hand = five_cards
                    best_rank = HandRank.STRAIGHT
            
            # Three of a Kind
            three_kind = HandEvaluator._is_three_of_kind(five_cards)
            if three_kind:
                if not best_rank or best_rank.value < HandRank.THREE_OF_A_KIND.value:
                    best_hand = three_kind
                    best_rank = HandRank.THREE_OF_A_KIND
                    
            # Two Pair
            two_pair = HandEvaluator._is_two_pair(five_cards)
            if two_pair:
                if not best_rank or best_rank.value < HandRank.TWO_PAIR.value:
                    best_hand = two_pair
                    best_rank = HandRank.TWO_PAIR 
            
            # Pair
            pair = HandEvaluator._is_pair(five_cards)
            if pair:
                if not best_rank or best_rank.value < HandRank.PAIR.value:
                    best_hand = pair
                    best_rank = HandRank.PAIR
        
        # If no better hand was found, it's a high card
        if not best_rank:
            return HandRank.HIGH_CARD, sorted_cards[:5]
        
        return best_rank, list(best_hand)

    @staticmethod
    def _is_royal_flush(cards: List[Card]) -> bool:
        """Check if cards form a royal flush."""
        if not HandEvaluator._is_flush(cards):
            return False
        ranks = {card.rank for card in cards}
        royal_ranks = {Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE}
        return ranks == royal_ranks

    @staticmethod
    def _is_straight_flush(cards: List[Card]) -> bool:
        """Check if cards form a straight flush."""
        return HandEvaluator._is_flush(cards) and HandEvaluator._is_straight(cards)

    @staticmethod
    def _is_four_of_kind(cards: List[Card]) -> Optional[List[Card]]:
        """
        Check if cards contain four of a kind.
        Returns the four matching cards plus highest kicker if found.
        """
        rank_counts = Counter(card.rank for card in cards)
        for rank, count in rank_counts.items():
            if count == 4:
                four_cards = [card for card in cards if card.rank == rank]
                kickers = [card for card in cards if card.rank != rank]
                return four_cards + [kickers[0]]
        return None

    @staticmethod
    def _is_three_of_kind(cards: List[Card]) -> Optional[List[Card]]:
        """
        Check if cards contain three of a kind.
        Returns the three matching cards plus highest two kickers if found.
        """
        rank_counts = Counter(card.rank for card in cards)
        for rank, count in rank_counts.items():
            if count == 3:
                three_cards = [card for card in cards if card.rank == rank]
                kickers = [card for card in cards if card.rank != rank]
                return three_cards + sorted(kickers, key=lambda x: x.rank.value, reverse=True)[:2]
        return None
    
    @staticmethod
    def _is_two_pair(cards: List[Card]) -> Optional[List[Card]]:
        """
        Check if cards contain two pairs.
        Returns the two pairs plus highest kicker if found.
        """
        rank_counts = Counter(card.rank for card in cards)
        pairs = []
        kickers = []

        for rank, count in rank_counts.items():
            if count == 2:
                pairs.append(rank)
            elif count == 1:
                kickers.append(rank)

        if len(pairs) == 2: 
            two_cards = [card for card in cards if card.rank in pairs]
            kickers = [card for card in cards if card.rank not in pairs]
            return two_cards + sorted(kickers, key=lambda x: x.rank.value, reverse=True)[:1]
        return None
    
    @staticmethod
    def _is_pair(cards: List[Card]) -> Optional[List[Card]]:
        """
        Check if cards contain a pair.
        Returns the pair plus highest three kickers if found.
        """
        rank_counts = Counter(card.rank for card in cards)
        for rank, count in rank_counts.items():
            if count == 2:
                pair_cards = [card for card in cards if card.rank == rank]
                kickers = [card for card in cards if card.rank != rank]
                return pair_cards + sorted(kickers, key=lambda x: x.rank.value, reverse=True)[:3]
        return None

    @staticmethod
    def _is_full_house(cards: List[Card]) -> Optional[List[Card]]:
        """
        Check if cards form a full house.
        Returns the three matching cards plus the pair if found.
        """
        rank_counts = Counter(card.rank for card in cards)
        three_rank = None
        pair_rank = None
        
        for rank, count in rank_counts.items():
            if count == 3:
                three_rank = rank
            elif count == 2:
                pair_rank = rank
            
        if three_rank and pair_rank:
            three_cards = [card for card in cards if card.rank == three_rank]
            pair_cards = [card for card in cards if card.rank == pair_rank]
            return three_cards + pair_cards
        return None

    @staticmethod
    def _is_flush(cards: List[Card]) -> bool:
        """Check if all cards are the same suit."""
        return len({card.suit for card in cards}) == 1

    @staticmethod
    def _is_straight(cards: List[Card]) -> bool:
        """Check if cards form a straight."""
        ranks = sorted([card.rank.value for card in cards])
        
        # Check regular straight
        if ranks == list(range(ranks[0], ranks[0] + 5)):
            return True
        
        # Check Ace-low straight (A,2,3,4,5)
        if ranks == [2, 3, 4, 5, 14]:
            return True
        
        return False

    @staticmethod
    def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
        """Returns 1 if hand1 wins, -1 if hand2 wins, 0 if tie"""
        rank1, cards1 = HandEvaluator.evaluate_hand(hand1)
        rank2, cards2 = HandEvaluator.evaluate_hand(hand2)


        if rank1.value != rank2.value:
            return 1 if rank1.value > rank2.value else -1
        
        # Compare cards
        for card1, card2 in zip(cards1, cards2):
            if card1.rank.value != card2.rank.value:
                return 1 if card1.rank.value > card2.rank.value else -1
        
        return 0
        