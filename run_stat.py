from itertools import combinations
from run_game import GameRunner
from checkers.consts import TIE, BLACK_PLAYER, RED_PLAYER
import matplotlib.pyplot as plt
import csv

F_NAME = "experiments.csv"
PLAYERS_NAME = ["simple_player",
                "AI2_305030868_312434269.better_h_player",
                "AI2_305030868_312434269.improved_player",
                "AI2_305030868_312434269.improved_better_h_player"]

DISPLAY_PLAYERS_NAME = {"simple_player": "simple_player", "AI2_305030868_312434269.better_h_player": "better_h_player",
                        "AI2_305030868_312434269.improved_player": "improved_player",
                        "AI2_305030868_312434269.improved_better_h_player": "improved_better_h_player"}
T = [2, 10, 50]
# T = [2]
MOVES_PER_ROUND = 5
SETUP_TIME = 2
WINING_SCORE = 1
TIE_SCORE = 0.5
plt.rcParams["figure.figsize"] = 10, 15
plt.rcParams["legend.loc"] = "upper right"


def run_players():
    players_stat = {"simple_player": [0]*len(T),
                    "better_h_player": [0]*len(T),
                    "improved_player": [0]*len(T),
                    "improved_better_h_player": [0]*len(T)}

    with open(F_NAME, mode="w") as f_csv:
        csv_writer = csv.writer(f_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # for each time
        for j, t in enumerate(T):

            # all players combinations
            for player1, player2 in combinations(PLAYERS_NAME, 2):

                # each option make twice
                for i in range(2):
                    winner = GameRunner(SETUP_TIME, t, MOVES_PER_ROUND, "y", player1, player2).run()
                    score1 = 0
                    score2 = 0

                    # open tuple
                    if "tuple" in str(type(winner)):
                        winner = winner[0]

                    if winner == TIE:
                        players_stat[DISPLAY_PLAYERS_NAME[player1]][j] += TIE_SCORE
                        players_stat[DISPLAY_PLAYERS_NAME[player2]][j] += TIE_SCORE
                        score1 = TIE_SCORE
                        score2 = TIE_SCORE
                    elif winner == RED_PLAYER:
                        players_stat[DISPLAY_PLAYERS_NAME[player1]][j] += WINING_SCORE
                        score1 = WINING_SCORE
                    elif winner == BLACK_PLAYER:
                        players_stat[DISPLAY_PLAYERS_NAME[player2]][j] += WINING_SCORE
                        score2 = WINING_SCORE

                    csv_writer.writerow([DISPLAY_PLAYERS_NAME[player1], DISPLAY_PLAYERS_NAME[player2], t, score1, score2])
    plots = []
    # plot
    for player_name in players_stat:
        line, _ = plt.plot(T, players_stat[player_name], label=player_name)

    plt.title('Score as function of t')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    run_players()
