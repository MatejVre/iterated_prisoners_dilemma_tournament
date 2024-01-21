from Game import *
from Player import *
from Strategies import *
from Tournament import *
import matplotlib.pyplot as plt
import numpy as np
from Analisys import *

#This is the constant that represents the chance of failure
#It is expressed in %
class Controller():
    def __init__(self):
        self.s1 = AlwaysDefect()
        self.s2 = AlwaysCooperate()
        self.s3 = TitForTat()
        self.s4 = RandomChoice()
        self.s5 = Grofman()
        self.s6 = Shubik()
        self.s7 = GrimTrigger()
        self.s8 = Davis()
        self.s9 = Joss()
        
        self.tournament = None
        self.analisys = Analisys()

        self.basic_list_of_strategies = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9]
        self.custom_list_of_strategies = []

    def fill_with_basic_strategies(self):
        self.custom_list_of_strategies = self.basic_list_of_strategies

    def create_tournament(self, number_of_iterations):
        self.tournament = Tournament(self.custom_list_of_strategies, iterations=number_of_iterations)

    def clear_custom_list_of_strategies(self):
        self.custom_list_of_strategies = []

    def play_tournament(self):
        self.tournament.play_basic_tournament()
        self.analisys.set_strategy_score_data(self.tournament.strategy_scores)
        self.analisys.set_tournament_history_data(self.tournament.tournament_history)

    def table_of_averages(self):
        self.analisys.create_table_of_averages()

    def clear(self):
        self.tournament = None
        self.analisys = Analisys()

"""
print(tournament.tournament_history)
print(tournament.strategy_scores)
analisys.set_strategy_score_data(tournament.strategy_scores)
analisys.set_tournament_history_data(tournament.tournament_history)
print(analisys.create_table_of_averages())
print(analisys.create_history_table())
print(analisys.get_strategy_history("RandomChoice"))
print(analisys.create_strategy_history_table("Joss"))

#s7 = AlwaysDefect(chance_of_inverse=COI)
#s8 = AlwaysCooperate(chance_of_inverse=COI)
#s9 = TitForTat(chance_of_inverse=COI)
#s10 = RandomChoice(chance_of_inverse=COI)
#s11 = Grofman(chance_of_inverse=COI)
#s12 = Shubik(chance_of_inverse=COI)


listOfStrategies2 = [s7, s8, s9, s10, s11, s12]




values1 = list(tournament.strategy_scores.values())


tournament_with_failures = Tournament(game, listOfStrategies2)
tournament_with_failures.play_basic_tournament()
values2 = list(tournament_with_failures.strategy_scores.values())
print(tournament.get_strategy_history("TitForTat"))

names = list(tournament.strategy_scores.keys())

X_axis = np.arange(len(names))

plt.bar(X_axis , values1, 0.2, label="Regular strategies")
plt.bar(X_axis + 0.2, values2, 0.2, label="Strategies with a 5 percent chance of error")

plt.title("Tournament results")
plt.xticks(X_axis, names)
plt.xlabel("Strategies")
plt.ylabel("Score")
plt.legend()
plt.show()

"""

#print(game.addServedTime())
#print(game.player_moves)
#game.clear_player_moves()
#print(game.player_moves)

#print(game.game_history)