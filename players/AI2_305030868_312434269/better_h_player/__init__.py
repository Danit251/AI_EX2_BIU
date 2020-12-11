import abstract
from players.simple_player import Player as SimpleP
from checkers.consts import PAWN_COLOR, KING_COLOR, OPPONENT_COLOR, MAX_TURNS_NO_JUMP, BOARD_ROWS, BACK_ROW
from utils import INFINITY

KING_SCORE = 2


class Player(SimpleP):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        SimpleP.__init__(self, setup_time, player_color, time_per_k_turns, k)

    def utility(self, state):
        if len(state.get_possible_moves()) == 0:
            return INFINITY if state.curr_player != self.color else -INFINITY

        if state.turns_since_last_jump >= MAX_TURNS_NO_JUMP:
            return 0

        player_u, opponent_u = self.get_players_utility(state.board)

        if player_u == 0:
            # I have no tools left
            return -INFINITY
        elif opponent_u == 0:
            # The opponent has no tools left
            return INFINITY
        else:
            return player_u - opponent_u

    def get_players_utility(self, board):
        my_score = 0
        opponent_score = 0
        opponent_color = OPPONENT_COLOR[self.color]

        for (row, col), val in board.items():
            # my pawn
            if val == PAWN_COLOR[self.color]:
                my_score += abs(BACK_ROW[self.color] - row) + 1

            # opponent's pawn
            if val == PAWN_COLOR[opponent_color]:
                opponent_score += abs(BACK_ROW[opponent_color] - row) + 1

            # my king
            if val == KING_COLOR[self.color]:
                my_score += BOARD_ROWS * KING_SCORE

            # opponent's king
            if val == KING_COLOR[opponent_color]:
                opponent_score += BOARD_ROWS * KING_SCORE

        return my_score, opponent_score

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better h player')
