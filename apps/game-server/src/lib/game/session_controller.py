from enum import Enum

from web_poker.game.game_controller import GameController
from web_poker.models.deck import Deck

class Position(Enum):
    BUTTON = "BTN"
    SMALL_BLIND = "SB"
    BIG_BLIND = "BB"
    
class SessionController:
    def __init__(self):
        self.game_counter = 0
        self.players = []
        self.deck = Deck()
        self.button_index = 0
        
    def add_player(self, player):
        if len(self.players) >= self.max_players:
            raise ValueError("Cannot add more players. Maximum allowed: 9")
        self.players.append(player)
        
    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
        else:
            raise ValueError("Player not found in game")
        
    def assign_positions(self):
        """Assign positions (BTN, SB, BB) based on number of players."""
        num_players = len(self.players)
        if num_players < 2:
            return
            
        # Clear all positions
        for player in self.players:
            player.set_position(None)
            
        # Assign button
        self.players[self.button_index].set_position(Position.BUTTON)
        
        if num_players == 2:
            # Heads-up play: BTN is SB, other player is BB
            sb_index = self.button_index
            bb_index = (self.button_index + 1) % num_players
        else:
            # 3+ players: BTN, SB, BB in sequence
            sb_index = (self.button_index + 1) % num_players
            bb_index = (self.button_index + 2) % num_players
            
        self.players[sb_index].set_position(Position.SMALL_BLIND)
        self.players[bb_index].set_position(Position.BIG_BLIND)
  
    def start_session(self):
        self.game_controller = GameController(self.players)
        
        
        self.assign_positions()
        self.game_controller.start_game()
        
    def proceed_session(self):
        self.game_controller.start_game()

    def end_session(self):
        self.game_controller.end_game()
        self.settle_session()
    
    def settle_session(self):
        # TODO: Implement session settlement, remove players from session
        pass

    
    