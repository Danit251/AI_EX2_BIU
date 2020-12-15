import abstract
from players.simple_player import Player as SimpleP
from checkers.consts import PAWN_COLOR, KING_COLOR, OPPONENT_COLOR, MAX_TURNS_NO_JUMP, BOARD_ROWS, BACK_ROW, EM
from utils import INFINITY

KING_SCORE = 1.5


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
                my_score += self.pawn_score(self.color, board, row, col)

            # opponent's pawn
            elif val == PAWN_COLOR[opponent_color]:
                my_score += self.pawn_score(opponent_color, board, row, col)

            # my king
            elif val == KING_COLOR[self.color]:
                my_score += self.king_score(row, col)

            # opponent's king
            elif val == KING_COLOR[opponent_color]:
                opponent_score += self.king_score(row, col)

        # my_score += self.bonus_safe_king(board, my_kings_loc)
        # opponent_score += self.bonus_safe_king(board, opponent_kings_loc)

        # if not pawn_exists:
            # print("There is no pawn!!!")
            # print(board.items())
            # distance = 0
            # print(my_kings_loc, opponent_kings_loc)
            # for my_king in my_kings_loc:
            #     for opp_king in opponent_kings_loc:
            #         distance += abs(opp_king[0] - my_king[0]) + abs(opp_king[1] - my_king[1])
            # if my_score >= opponent_score:
            #     opponent_score += distance
            # else:
            #     my_score += distance

        return my_score, opponent_score

    def bonus_safe_king(self, row, col):
        bonus = 0
        # for (row, col) in kings_loc:
        if any([row == BACK_ROW[self.color],
                row == BACK_ROW[OPPONENT_COLOR[self.color]],
                col == BACK_ROW[self.color],
                col == BACK_ROW[OPPONENT_COLOR[self.color]]]):
            bonus += BOARD_ROWS * 0.5
        return bonus

    def pawn_score(self, player_color, board, row, col):
        score = 0

        if any([row == BACK_ROW[OPPONENT_COLOR[player_color]],
                col == BACK_ROW[OPPONENT_COLOR[player_color]],
                col == BACK_ROW[player_color]]):
            score += 1.5
        # elif board[row-1, col-1] != EM and board[row-1, col+1] != EM:
        #     score += 1.5
        # elif board[row-1, col-1] != EM or board[row-1, col+1] != EM:
        #     score += 0.5

        score += abs(BACK_ROW[self.color] - row) + 1

        return score

    def king_score(self, row, col):
        score = BOARD_ROWS * KING_SCORE
        score += self.bonus_safe_king(row, col)
        return score

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better h player')
