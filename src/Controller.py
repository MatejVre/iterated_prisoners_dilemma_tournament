import copy
from Game import *
from Player import *
from Strategies import *
from Tournament import *
import matplotlib.pyplot as plt
import numpy as np
from Analisys import *

#This is the constant that represents the chance of failure
#It is expressed in %
class Controller():
    def __init__(self):
        self.s1 = AlwaysDefect()
        self.s2 = AlwaysCooperate()
        self.s3 = TitForTat()
        self.s4 = RandomChoice()
        self.s5 = Grofman()
        self.s6 = Shubik()
        self.s7 = GrimTrigger()
        self.s8 = Davis()
        self.s9 = Joss()
        
        self.tournament = None
        self.analisys = Analisys()

        self.basic_list_of_strategies = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9]
        self.custom_list_of_strategies = []

    def fill_with_basic_strategies(self):
        for strat in self.basic_list_of_strategies:
            self.add_strategy(strat.name(), 0)

    def create_tournament(self, number_of_iterations):
        #python passes arguments as object reference, so i have to create a copy by value to give to the tournament
        #so i have a clear distinction between the strategies in the tournament and strategies to be added
        used_strategies = self.custom_list_of_strategies[:]
        self.tournament = Tournament(used_strategies, iterations=number_of_iterations)

    def clear_custom_list_of_strategies(self):
        self.custom_list_of_strategies = []

    def play_tournament(self):
        self.tournament.reset()
        self.tournament.play_basic_tournament()
        self.analisys.set_strategy_score_data(self.tournament.strategy_scores)
        self.analisys.set_tournament_history_data(self.tournament.tournament_history)

    def table_of_averages(self):
        self.analisys.create_table_of_averages()

    def clear(self):
        self.tournament = None
        self.analisys = Analisys()
        self.custom_list_of_strategies = []

    def add_strategy(self, name, COI):
        strategy_creator = {}
        for strat in self.basic_list_of_strategies:
            strategy_creator[strat.name()] = strat
        strategy = copy.copy(strategy_creator[name])
        strategy.set_COI(int(COI))
        #check if there are two of the same (strategy, COI) combination
        list_of_current_names = [s.name() for s in self.custom_list_of_strategies]
        if strategy.name() in list_of_current_names:
            self.name_strategy(strategy)
        self.custom_list_of_strategies.append(strategy)
        return(strategy)
    
    #called if there are two of the same (strategy, COI) combination
    def name_strategy(self, strat):
        strategy_name = strat.name()
        counter = 1
        returned_name = strategy_name + f"-{counter}"
        list_of_current_names = [s.name() for s in self.custom_list_of_strategies]
        while returned_name in list_of_current_names:
            counter += 1
            returned_name = strategy_name + f"-{counter}"
        strat.set_given_name(returned_name)
        return returned_name
        
