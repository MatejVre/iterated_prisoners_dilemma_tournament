import copy
from Game import Game
from Strategies import *
import itertools
from Errors import TournamentSizeError

class Tournament():


    def __init__(self):
        print("init")
        self.game = Game()
        self.list_of_strategies = []
        self.iterations = 200
        self.tournament_history = {}
        self.strategy_scores = {}


    def play_basic_tournament(self):
        game = self.game
        #plays all the different combinations of strategy pairs
        if len(self.list_of_strategies) < 2:
            raise TournamentSizeError("Tournament has to have at least 2 strategies!")
        else:
            for strategy_pair in self.get_unique_strategy_pairs():
                strat1 = strategy_pair[0]
                strat2 = strategy_pair[1]
                game.strategy1 = strat1
                game.strategy2 = strat2
                print("Playing %s against %s" %(strat1.name(), strat2.name()))
                for i in range(self.iterations):
                    game.play_round()
                strat1.reset()
                strat2.reset()
                score = game.add_payoffs()
                self.tournament_history[(strat1.name(), strat2.name())] = score
                self.add_strategy_score(strat1, score[0])
                self.add_strategy_score(strat2, score[1])
                game.clear()
            #each strategy plays with a COPY of itself. Not itself directly because that would cause conflicts the world is not ready for
            for strategy in self.list_of_strategies:
                strat1 = strategy
                strat2 = copy.copy(strategy)
                game.strategy1 = strat1
                game.strategy2 = strat2
                print("Playing %s against %s" %(strat1.name(), strat2.name()))
                for i in range(self.iterations):
                    game.play_round()
                strat1.reset()
                strat2.reset()
                score = game.add_payoffs()
                self.tournament_history[(strat1.name(), strat2.name())] = score
                self.add_strategy_score(strat1, score[0])
                game.clear()

    #test?? Do i have to test a call to an integrated method??
    def get_unique_strategy_pairs(self):
        return itertools.combinations(self.list_of_strategies, 2)
    

    def reset(self):
        self.tournament_history = {}
        self.strategy_scores = {}


    def add_strategy(self, strategy):
        self.list_of_strategies.append(strategy)

    
    def remove_strategy(self, strategy):
        try:
            self.list_of_strategies.remove(strategy)
            self.reset()
        except ValueError:
            print("Strategy is not in the list of strategies")
    

    def set_iterations(self, number):
        self.iterations = number
    

    def add_strategy_score(self, strategy, score):
        if strategy.name() not in self.strategy_scores.keys():
            self.strategy_scores[strategy.name()] = score
        else:
            self.strategy_scores[strategy.name()] += score