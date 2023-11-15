from Game import Game
from Strategies import *
import itertools

class Tournament():

    def __init__(self, game: Game, listOfStrategies):
        self.game = game
        self.listOfStrategies = listOfStrategies


    def play_basic_tournament(self):
        game = self.game
        for strategy_pair in self.get_unique_strategy_pairs():
            game.strategy1 = strategy_pair[0]
            game.strategy2 = strategy_pair[1]
            print("Playing %s against %s" %(strategy_pair[0].name(), strategy_pair[1].name()))
            for i in range(100):
                game.playGame()
            print(game.addServedTime())
            game.clear_game_history()
            game.clear_player_moves()

            
    

    def get_unique_strategy_pairs(self):
        return itertools.combinations_with_replacement(self.listOfStrategies, 2)

#t = Tournament(Game(), [TitForTat(), AlwaysCooperate(), AlwaysDefect(), RandomChoice()])
#strats = t.get_unique_strategy_pairs()
#for s in strats:
#    print(s[0].name(), s[1].name())
