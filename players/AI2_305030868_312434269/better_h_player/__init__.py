import abstract
from players.simple_player import Player as SimpleP
from checkers.consts import PAWN_COLOR, KING_COLOR, OPPONENT_COLOR, MAX_TURNS_NO_JUMP, BOARD_ROWS
from utils import INFINITY


class Player(SimpleP):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        SimpleP.__init__(self, setup_time, player_color, time_per_k_turns, k)

    def utility(self, state):
        if len(state.get_possible_moves()) == 0:
            return INFINITY if state.curr_player != self.color else -INFINITY

        if state.turns_since_last_jump >= MAX_TURNS_NO_JUMP:
            return 0

        player_u = self.get_player_utility(state.board)
        opponent_u = self.get_opponent_utility(state.board)

        if player_u == 0:
            # I have no tools left
            return -INFINITY
        elif opponent_u == 0:
            # The opponent has no tools left
            return INFINITY
        else:
            return player_u - opponent_u

    def get_player_utility(self, board):
        score = 0
        for (row, col), val in board.items():
            if val == PAWN_COLOR[self.color]:
                score += row + 1
            if val == KING_COLOR[self.color]:
                score += BOARD_ROWS
        return score

    def get_opponent_utility(self, board):
        score = 0
        opponent_color = OPPONENT_COLOR[self.color]

        for (row, col), val in board.items():
            if val == PAWN_COLOR[opponent_color]:
                score += BOARD_ROWS - row + 1
            if val == KING_COLOR[opponent_color]:
                score += BOARD_ROWS
        return score

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better h player')
