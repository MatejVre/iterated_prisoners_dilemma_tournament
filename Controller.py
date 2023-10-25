from Game import *
from Player import *

def alwaysDefect():
    return 1

def alwaysCooperate():
    return 0


#expected return: (0, 3)
player1 = Player(alwaysDefect)
player2 = Player(alwaysCooperate)
game = Game(player1, player2)

for i in range(10):
    game.playGame()

print(game.player_moves)
print(game.game_history)