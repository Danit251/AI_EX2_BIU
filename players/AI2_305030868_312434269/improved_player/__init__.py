import abstract
from players.simple_player import Player as SimpleP
import time
from utils import MiniMaxWithAlphaBetaPruning, INFINITY, run_with_limited_time, ExceededTimeError


class Player(SimpleP):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        SimpleP.__init__(self, setup_time, player_color, time_per_k_turns, k)

    def get_move(self, game_state, possible_moves):
        self.clock = time.process_time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05

        # Choosing an arbitrary move in case Minimax does not return an answer:
        best_move = possible_moves[0]

        if len(possible_moves) == 1:
            return possible_moves[0]
        else:
            # if there is only one jump return it
            one_jump = False
            for possible_m in possible_moves:
                if len(possible_m.jumped_locs) > 0 and not one_jump:
                    one_jump = True
                    best_move = possible_m

                if len(possible_m.jumped_locs) > 0 and one_jump:
                    one_jump = False
                    best_move = possible_moves[0]
                    break

            if one_jump:
                return best_move

        current_depth = 1
        prev_alpha = -INFINITY

        # Initialize Minimax algorithm, still not running anything
        minimax = MiniMaxWithAlphaBetaPruning(self.utility, self.color, self.no_more_time,
                                              self.selective_deepening_criterion)

        prev_move = None
        move_repeat = 0
        # Iterative deepening until the time runs out.
        while True:

            print('going to depth: {}, remaining time: {}, prev_alpha: {}, best_move: {}'.format(
                current_depth,
                self.time_for_current_move - (time.process_time() - self.clock),
                prev_alpha,
                best_move))

            try:
                (alpha, move), run_time = run_with_limited_time(
                    minimax.search, (game_state, current_depth, -INFINITY, INFINITY, True), {},
                    self.time_for_current_move - (time.process_time() - self.clock))
            except (ExceededTimeError, MemoryError):
                print('no more time, achieved depth {}'.format(current_depth))
                break

            if self.no_more_time():
                print('no more time')
                break

            if alpha == prev_alpha and move.origin_loc == prev_move.origin_loc and move.target_loc == prev_move.target_loc:
                if len(move.jumped_locs) > 0 or move_repeat == 3:
                    best_move = move
                    break

                move_repeat += 1

            # if it doesn't repeat the last move make counter zero
            if prev_move and not (move.origin_loc == prev_move.origin_loc and move.target_loc == prev_move.target_loc):
                move_repeat = 0

            prev_alpha = alpha
            prev_move = move
            best_move = move

            if alpha == INFINITY:
                print('the move: {} will guarantee victory.'.format(best_move))
                break

            if alpha == -INFINITY:
                print('all is lost')
                break

            current_depth += 1

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.process_time() - self.clock)
        return best_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'improved player')
