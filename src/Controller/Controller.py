import copy
from Model.Game import *
from Model.Strategies import *
from Model.Tournament import *
from Model.Analisys import *
from Model.Errors import TournamentSizeError

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
        self.s10 = Tullock()
        self.s11 = Anklebreaker()
        self.s12 = Adapter()
        self.s13 = TitForTwoTats()

        
        self.tournament = Tournament()
        self.analisys = Analisys()

        self.basic_list_of_strategies = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13]
        
        self.strategy_creator = {}
        for strat in self.basic_list_of_strategies:
            self.strategy_creator[strat.name()] = strat


    def fill_with_basic_strategies(self, COI):
        for strat in self.basic_list_of_strategies:
            self.add_strategy(strat.name(), COI)

    
    def play_tournament(self):
        self.tournament.reset()
        self.tournament.play_basic_tournament()
        self.analisys.set_strategy_score_data(self.tournament.strategy_scores)
        self.analisys.set_tournament_history_data(self.tournament.tournament_history)
        self.analisys.set_matchup_move_history_data(self.tournament.strategy_move_history)

    #call to other method, no need for testing
    def table_of_averages(self, ordering):
        return self.analisys.create_table_of_averages(ordering)
    
    #call to other method, no need for testing
    def history_table(self):
        return self.analisys.create_history_table()
    
    #call to other method, no need for testing
    def strategy_history_table(self, search):
        return self.analisys.create_strategy_history_table(search)
    
    #call to other method, no need for testing
    def matchup_move_history_table(self, strategy1, strategy2):
        return self.analisys.create_matchup_move_history_table(strategy1, strategy2)

    #call to other method, no need for testing
    def clear(self):
        self.tournament = Tournament()
        self.analisys = Analisys()

    #tested
    def add_strategy(self, name, COI):
        
        strategy = copy.copy(self.strategy_creator[name])
        strategy.set_COI(int(COI))
        #check if there are two of the same (strategy, COI) combination
        list_of_current_names = [s.name() for s in self.tournament.list_of_strategies]
        if strategy.name() in list_of_current_names:
            self.name_strategy(strategy)
        self.tournament.add_strategy(strategy)
        return(strategy)
    
    #called if there are two of the same (strategy, COI) combination
    #tested
    def name_strategy(self, strat):
        strategy_name = strat.name()
        counter = 1
        returned_name = strategy_name + f"-{counter}"
        list_of_current_names = [s.name() for s in self.tournament.list_of_strategies]
        while returned_name in list_of_current_names:
            counter += 1
            returned_name = strategy_name + f"-{counter}"
        strat.set_given_name(returned_name)
        return returned_name
    

    #The two methods defined below are very similar but one has to throw an error if 
    def remove_strategy_from_tournament(self, name):
        for strategy in self.tournament.list_of_strategies:
            if strategy.name() == name:
                self.tournament.list_of_strategies.remove(strategy)
                return True
        return False
    

    def set_iterations(self, input):
        if str(input).isnumeric():
            if int(input) >= 1 and int(input) <= 10000:
                self.set_tournament_iterations(int(input))
                return True
        return False

    #call to other method, no need for testing
    def set_tournament_iterations(self, number):
        self.tournament.set_iterations(number)
        self.analisys = Analisys()

