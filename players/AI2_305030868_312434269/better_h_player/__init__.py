import abstract
from players.simple_player import Player as SimpleP
from checkers.consts import PAWN_COLOR, KING_COLOR, OPPONENT_COLOR, MAX_TURNS_NO_JUMP, BOARD_ROWS, BACK_ROW, EM
from utils import INFINITY
import numpy as np

KING_SCORE = 2.2


class Player(SimpleP):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        SimpleP.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.going_forward = self.is_going_forward(player_color)

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
        middle = BOARD_ROWS * 0.5
        # board_vals = np.array(list(board.values()))
        # board_occurrences = dict(zip(np.unique(board_vals, PAWN_COLOR[self.color])))
        # my_score += (board_vals == PAWN_COLOR[self.color]).sum()
        for (row, col), val in board.items():
            # my pawn
            if val == PAWN_COLOR[self.color]:
                # my_score += self.pawn_score(self.color, board, row, col)
                if self.going_forward:
                    if row >= middle - 1:
                        my_score += 7
                    else:
                        my_score += 5
                else:
                    if row >= middle - 1:
                        my_score += 5
                    else:
                        my_score += 7
            # opponent's pawn
            elif val == PAWN_COLOR[opponent_color]:
                # opponent_score += self.pawn_score(opponent_color, board, row, col)
                if self.going_forward:
                    if row >= middle - 1:
                        my_score += 5
                    else:
                        my_score += 7
                else:
                    if row >= middle - 1:
                        my_score += 7
                    else:
                        my_score += 5
            # my king
            elif val == KING_COLOR[self.color]:
                # my_score += self.king_score(board, self.color, row, col)
                my_score += 10

            # opponent's king
            elif val == KING_COLOR[opponent_color]:
                # opponent_score += self.king_score(board, self.color, row, col)
                opponent_score += 10

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

    def is_going_forward(self, player_color):
        if BACK_ROW[player_color] > BACK_ROW[OPPONENT_COLOR[player_color]]:
            return True
        return False

    def bonus_safe_king(self, row, col):
        bonus = 0
        # for (row, col) in kings_loc:
        if any([row == BACK_ROW[self.color],
                row == BACK_ROW[OPPONENT_COLOR[self.color]],
                col == BACK_ROW[self.color],
                col == BACK_ROW[OPPONENT_COLOR[self.color]]]):
            bonus += BOARD_ROWS * 0.5
        return bonus

    def bonus_defense(self, board, player_color, row, col):
        score = 0
        board_vals = list(board.values())
        if board_vals.count(KING_COLOR[OPPONENT_COLOR[player_color]]) <= 1:
            if BACK_ROW[player_color] > BACK_ROW[OPPONENT_COLOR[player_color]]:
                if row != 0:
                    if (col == BACK_ROW[OPPONENT_COLOR[player_color]] or board[row-1, col-1] != EM) and \
                       (col == BACK_ROW[player_color] or board[row-1, col+1] != EM):
                        score += 2.5
                    elif (col == BACK_ROW[OPPONENT_COLOR[player_color]] or board[row-1, col-1] != EM) or \
                         (col == BACK_ROW[player_color] or board[row-1, col+1] != EM):
                        score += 1.5
            else:
                if row != BACK_ROW[OPPONENT_COLOR[player_color]]:
                    if (col == BACK_ROW[OPPONENT_COLOR[player_color]] or board[row+1, col+1] != EM) and \
                       (col == BACK_ROW[player_color] or board[row+1, col-1] != EM):
                        score += 2.5
                    elif (col == BACK_ROW[OPPONENT_COLOR[player_color]] or board[row+1, col+1] != EM) or \
                         (col == BACK_ROW[player_color] or board[row+1, col-1] != EM):
                        score += 1.5
        return score

    def pawn_score(self, player_color, board, row, col):
        score = 0
        board_vals = list(board.values())
        if PAWN_COLOR[OPPONENT_COLOR[player_color]] in board_vals and any([row == BACK_ROW[OPPONENT_COLOR[player_color]],
                                                                           col == BACK_ROW[OPPONENT_COLOR[player_color]],
                                                                           col == BACK_ROW[player_color]]):
            score += 1.5

        score += self.bonus_defense(board, player_color, row, col)
        pawn_score = abs(BACK_ROW[self.color] - row) + 1
        if board_vals.count(PAWN_COLOR[player_color]) <= board_vals.count(KING_COLOR[player_color]):
            pawn_score *= 2

        score += pawn_score
        return score

    def king_score(self, board, player_color, row, col):
        score = BOARD_ROWS * KING_SCORE
        score += self.bonus_safe_king(row, col)
        score += self.bonus_defense(board, player_color, row, col)
        return score

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better h player')
