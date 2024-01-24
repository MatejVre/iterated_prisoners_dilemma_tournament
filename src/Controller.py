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
        self.custom_list_of_strategies.extend(self.basic_list_of_strategies)

    def create_tournament(self, number_of_iterations):
        self.tournament = Tournament(self.custom_list_of_strategies, iterations=number_of_iterations)

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

    def add_strategy(self, name, COI):
        strategy_creator = {}
        for strat in self.basic_list_of_strategies:
            strategy_creator[strat.name()] = strat
        strategy = copy.copy(strategy_creator[name])
        strategy.set_COI(int(COI))
        self.custom_list_of_strategies.append(strategy)
        return(strategy)
        
