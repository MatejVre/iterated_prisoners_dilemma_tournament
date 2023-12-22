from Game import *
from Player import *
from Strategies import *
from Tournament import *
import matplotlib.pyplot as plt
import numpy as np

#This is the constant that represents the chance of failure
#It is expressed in %
terminated = False
COI = 5

s1 = AlwaysDefect()
s2 = AlwaysCooperate()
s3 = TitForTat()
s4 = RandomChoice()
s5 = Grofman()
s6 = Shubik()

listOfStrategies = [s1, s2, s3, s4, s5, s6]
game = Game()
tournament = Tournament(game, listOfStrategies)

print("Implemented basic tournament with the following strategies with all strategies")

while not terminated:
    inp = input(":")
    if inp == "run":
        tournament.play_basic_tournament()
    elif inp == "results":
        print(tournament.tournament_history)
    else:
        print("wrong")

#s7 = AlwaysDefect(chance_of_inverse=COI)
#s8 = AlwaysCooperate(chance_of_inverse=COI)
#s9 = TitForTat(chance_of_inverse=COI)
#s10 = RandomChoice(chance_of_inverse=COI)
#s11 = Grofman(chance_of_inverse=COI)
#s12 = Shubik(chance_of_inverse=COI)

"""
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