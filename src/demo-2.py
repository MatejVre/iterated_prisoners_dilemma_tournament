from Game import *
from Player import *
from Strategies import *
from Tournament import *
from Analisys import *
import matplotlib.pyplot as plt
import numpy as np

#strategy initialisation
s1 = AlwaysDefect()
s2 = AlwaysCooperate()
s3 = TitForTat()
s4 = RandomChoice()
s5 = Grofman()
s6 = Shubik()
s7 = GrimTrigger()

#other initialisation
listOfStrategies = [s1, s2, s3, s4, s5, s6, s7]
tournament = Tournament(listOfStrategies)
tournament.play_basic_tournament()

s8 = AlwaysDefect(chance_of_inverse=5)
s9 = AlwaysCooperate(chance_of_inverse=5)
s10 = TitForTat(chance_of_inverse=5)
s11 = RandomChoice(chance_of_inverse=5)
s12 = Grofman(chance_of_inverse=5)
s13 = Shubik(chance_of_inverse=5)
s14 = GrimTrigger(chance_of_inverse=5)

listOfStrategies2 = [s8, s9, s10, s11, s12, s13, s14]




values1 = list(tournament.strategy_scores.values())


tournament_with_failures = Tournament(listOfStrategies2)
tournament_with_failures.play_basic_tournament()
values2 = list(tournament_with_failures.strategy_scores.values())


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