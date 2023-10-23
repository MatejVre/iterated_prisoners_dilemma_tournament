from Game import *
from Player import *

def alwaysDefect():
    return 1

def alwaysCooperate():
    return 0

game = Game()
player1 = Player(alwaysDefect)
player2 = Player(alwaysCooperate)

game.playGame(player1.chooseMove(), player2.chooseMove())