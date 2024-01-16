from Game import *
from Player import *
from Strategies import *
from Tournament import *
from Analisys import *

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
analisys = Analisys()

#setting tournament data
tournament.play_basic_tournament()
analisys.set_strategy_score_data(tournament.strategy_scores)
analisys.set_tournament_history_data(tournament.tournament_history)

#analisys part
print(analisys.create_table_of_averages())
print(analisys.create_history_table())
print(analisys.create_strategy_history_table("RandomChoice"))