from Game import *
from Player import *
from Strategies import *


strategy1 = AlwaysDefect()
strategy2 = AlwaysCooperate()
strategy3 = TitForTat()
strategy4 = RandomChoice()

game = Game(strategy4, strategy3)

for i in range(100):
    game.playGame()


print(game.addServedTime())
#print(game.player_moves)
#print(game.game_history)