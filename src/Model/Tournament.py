import copy
from Model.Game import Game
from Model.Strategies import *
import itertools
from Model.Errors import TournamentSizeError

class Tournament():


    def __init__(self):
        print("init")
        #Used to store the strategies playing in the tournament.
        self.list_of_strategies = []
        self.iterations = 200

        #Dictionary storing all of the played matches and their scores.
        #Shape: {(strategy1, strategy2): [score_by_strategy1, score_by_strategy2]}
        self.tournament_history = {}

        #Dictionary storing the move history of strategies.
        #Shape: {strategy1: {strategy2: moves, strategy3: moves}, strategy2: {...}, ...}
        #The dictionary above represents the moves strategy1 chose against strategy2 and strategy3.
        #Note: for games between two of the same strategies there is an exception -> strategy1: {strategy1: [moves1, moves2]}
        #Without the exception the moves stored would always be the same for both strategies due to how storing is done.
        #Possible future fix: make specific object keys instead of strategy names. This was already done in the game class.
        self.strategy_move_history = {}

        #Dictionary storing the scores which the strategies achieved.
        #Shape: {strategy: total_score}
        self.strategy_scores = {}
        self.strategy_matches = {}


    #this is quite a long method but it would make no sense to split it into.
    #2 smaller methods. Introduces chances for error which aren't necessary!
    def play_basic_tournament(self):
        #plays all the different combinations of strategy pairs
        if len(self.list_of_strategies) < 2:
            raise TournamentSizeError("Tournament has to have at least 2 strategies!")
        else:
            self.initialize_strategy_move_history()
            self.initialize_strategy_matches()
            for strategy_pair in self.get_unique_strategy_pairs():
                strat1 = strategy_pair[0]
                strat2 = strategy_pair[1]
                game = Game(strat1, strat2)
                #print("Playing %s against %s" %(strat1.name(), strat2.name()))
                for i in range(self.iterations):
                    game.play_round()
                strat1.reset()
                strat2.reset()
                score = game.add_payoffs()
                self.tournament_history[(strat1.name(), strat2.name())] = score
                self.add_strategy_moves(game, strat1, strat2)
                self.add_strategy_score(strat1, score[0])
                self.add_strategy_score(strat2, score[1])
                self.strategy_matches[strat1.name()][strat2.name()] = score[0]
                self.strategy_matches[strat2.name()][strat1.name()] = score[1]
                game.clear()
            for strategy in self.list_of_strategies:
                strat1 = strategy
                strat2 = copy.copy(strategy)
                game = Game(strat1, strat2)
                #print("Playing %s against %s" %(strat1.name(), strat2.name()))
                for _ in range(self.iterations):
                    game.play_round()
                strat1.reset()
                strat2.reset()
                score = game.add_payoffs()
                self.tournament_history[(strat1.name(), strat2.name())] = score
                self.add_strategy_moves(game, strat1, strat2)
                self.add_strategy_score(strat1, score[0])
                self.strategy_matches[strat1.name()][strat2.name()] = score[0]
                game.clear()

                
    #Creates pairings for matches. No combinations with repetitions
    #to avoid shared memory conflicts.
    def get_unique_strategy_pairs(self):
        return itertools.combinations(self.list_of_strategies, 2)
    

    #Resets the tournament to initial state.
    def reset(self):
        self.tournament_history = {}
        self.strategy_move_history = {}
        self.strategy_scores = {}
        self.strategy_matches = {}


    #Adds strategy to the tournament.
    #Strategy name added in Controller.
    def add_strategy(self, strategy):
        self.list_of_strategies.append(strategy)

    
    #Removes strategy from the tournament.
    def remove_strategy(self, strategy):
        try:
            self.list_of_strategies.remove(strategy)
            self.reset()
        except ValueError:
            print("Strategy is not in the list of strategies")
    

    #Sets rounds or iterations to the specified amount.
    def set_iterations(self, number):
        self.iterations = number
    

    #Appropriately adds the score to its corresponding strategy.
    #This is called after a game is completed to store scores.
    def add_strategy_score(self, strategy, score):
        if strategy.name() not in self.strategy_scores.keys():
            self.strategy_scores[strategy.name()] = score
        else:
            self.strategy_scores[strategy.name()] += score


    #Initializes the strategy move history dictionary
    def initialize_strategy_move_history(self):
        self.strategy_move_history = {}
        for strategy in self.list_of_strategies:
            self.strategy_move_history[strategy.name()] = dict()


    #Appropriately adds the strategy moves to its corresponding matchup.
    #This is called after a game is completed to store moves.
    def add_strategy_moves(self, game, strategy1, strategy2):
        moves = game.player_moves
        if strategy1.name() == strategy2.name():
            self.strategy_move_history[strategy1.name()][strategy2.name()] = [moves[strategy1], moves[strategy2]]
        else:
            self.strategy_move_history[strategy1.name()][strategy2.name()] = moves[strategy1]
            self.strategy_move_history[strategy2.name()][strategy1.name()] = moves[strategy2]


    #Initializes the strategy matches dictionary
    def initialize_strategy_matches(self):
        self.strategy_matches = {}
        for strategy in self.list_of_strategies:
            self.strategy_matches[strategy.name()] = dict()
