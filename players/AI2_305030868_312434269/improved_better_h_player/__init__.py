from players.simple_player import Player as SimpleP
from players.AI2_305030868_312434269.improved_player import Player as ImprovedP
from players.AI2_305030868_312434269.better_h_player import Player as BetterP
import abstract


class Player(BetterP):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        SimpleP.__init__(self, setup_time, player_color, time_per_k_turns, k)

    def get_move(self, game_state, possible_moves):
        return ImprovedP.get_move(self, game_state, possible_moves)

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'improved better h player')
