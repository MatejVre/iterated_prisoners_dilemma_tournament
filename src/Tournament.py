from Game import Game
from Strategies import *
import itertools

class Tournament():


    def __init__(self, listOfStrategies: [Strategy], **kwargs):
        self.game = Game()
        self.listOfStrategies = listOfStrategies
        self.iterations = 200
        self.tournament_history = {}
        self.strategy_scores = {}
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
                game.play_game()
            strat1.reset()
            strat2.reset()
            score = game.add_payoffs()
            self.tournament_history[(strat1.name(), strat2.name())] = score
            self.strategy_scores[strat1.name()] += score[0]
            self.strategy_scores[strat2.name()] += score[1]
            game.clear_game_history()
            game.clear_player_moves()

    #test?? Do i have to test a call to an integrated method??
    def get_unique_strategy_pairs(self):
        return itertools.combinations(self.listOfStrategies, 2)
    

    
    

    def reset(self):
        self.tournament_history = {}
        self.strategy_scores = {}