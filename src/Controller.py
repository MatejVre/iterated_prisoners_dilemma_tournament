from Game import *
from Player import *
from Strategies import *
from Tournament import *


s1 = AlwaysDefect()
s2 = AlwaysCooperate()
s3 = TitForTat()
s4 = RandomChoice()

listOfStrategies = [s1, s2, s3, s4]
game = Game()
tournament = Tournament(game, listOfStrategies)

tournament.play_basic_tournament()


#print(game.addServedTime())
#print(game.player_moves)
#game.clear_player_moves()
#print(game.player_moves)

#print(game.game_history)