from enum import Enum

from web_poker.models.deck import Deck
from web_poker.utils.constants import BIG_BLIND, SMALL_BLIND

class GameStatus(Enum):
    WAITING = "waiting"    # Waiting for players to join
    ACTIVE = "active"      # Game is in progress
    FINISHED = "finished"  # Game has ended

class BettingRound(Enum):
    PREFLOP = 0   # Initial betting round
    FLOP = 1      # After first 3 community cards
    TURN = 2      # After 4th community card
    RIVER = 3     # After 5th community card
    SHOWDOWN = 4  # Final round where players show cards
    
class GameController:
    def __init__(self, players):
      
        # status for the whole game
        self.players = players
        self.deck = Deck()
        
        # status for the current round
        self.pot = 0
        self.current_bet = 0
        self.current_player = 0
        self.game_status = GameStatus.WAITING
        self.betting_round = BettingRound.PREFLOP
            
    def start_game(self):
        """Start the game with the initial betting round."""
        self.deck.shuffle()
        self.pot = 0
        self.current_bet = 0
        self.current_player = 0
        self.round = 0
        self.game_status = GameStatus.ACTIVE
        
        # Deal initial cards
        for player in self.players:
            player.clear_hand()
            # Deal 2 cards to each player for Texas Hold'em
            player.add_card(self.deck.draw())
            player.add_card(self.deck.draw())
            
        # collect blinds
        self.collect_blinds()
    
    def _collect_blinds(self):
        """Collect small and big blinds from players."""
        if len(self.players) < 2:
            raise ValueError("Need at least 2 players to collect blinds")
            
        # Small blind is posted by the first player
        small_blind_player = self.players[0]
        small_blind_player.chips -= SMALL_BLIND
        self.pot += SMALL_BLIND
        
        # Big blind is posted by the second player
        big_blind_player = self.players[1] 
        big_blind_player.chips -= BIG_BLIND
        self.pot += BIG_BLIND
    
    def end_game(self):
        self.game_status = GameStatus.FINISHED
        self.pot = 0
        self.current_bet = 0
        self.current_player = 0
        self.round = 0
        # clear players hands
        for player in self.players:
            player.clear_hand()
