from Game import Game
from Strategies import *
import itertools

class Tournament():

    tournament_history = {}
    strategy_scores = {}

    def __init__(self, game: Game, listOfStrategies: [Strategy], **kwargs):
        self.game = game
        self.listOfStrategies = listOfStrategies
        self.iterations = 200
        for strat in listOfStrategies:
            self.strategy_scores[strat.name()] = 0
        #if the user specifies how many iterations per game, then play that many games
        #if not, play 200, as per Axelrod's paper
        if "iterations" in kwargs.keys():
            self.iterations = kwargs["iterations"]



    def play_basic_tournament(self):
        game = self.game
        for strategy_pair in self.get_unique_strategy_pairs():
            strat1 = strategy_pair[0]
            strat2 = strategy_pair[1]
            game.strategy1 = strat1
            game.strategy2 = strat2
            print("Playing %s against %s" %(strat1.name(), strat2.name()))
            for i in range(self.iterations):
                game.playGame()
            strat1.reset()
            strat2.reset()
            score = game.addServedTime()
            self.tournament_history[(strat1.name(), strat2.name())] = score
            self.strategy_scores[strat1.name()] += score[0]
            self.strategy_scores[strat2.name()] += score[0]
            game.clear_game_history()
            game.clear_player_moves()

    #test
    def get_unique_strategy_pairs(self):
        return itertools.combinations(self.listOfStrategies, 2)
    

    #test
    def get_strategy_history(self, strategy_name: str):
        strategy_history = {}
        for key in self.tournament_history.keys():
            if strategy_name in key:
                strategy_history[key] = self.tournament_history[key]
        if len(strategy_history) == 0:
            print("This strategy doesn't exist. Please check spelling!")
            return
        return strategy_history



#t = Tournament(Game(), [TitForTat(), AlwaysCooperate(), AlwaysDefect(), RandomChoice()])
#strats = t.get_unique_strategy_pairs()
#for s in strats:
#    print(s[0].name(), s[1].name())