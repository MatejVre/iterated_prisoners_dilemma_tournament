import copy
from Model.Game import *
from Model.Strategies import *
from Model.Tournament import *
from Model.Analisys import *
from Model.Errors import TournamentSizeError


class Controller():

    def __init__(self):

        self.tournament = Tournament()
        self.analisys = Analisys()

        #Used to create the strategy creator
        self.basic_list_of_strategies = [AlwaysDefect(), 
            AlwaysCooperate(), TitForTat(), RandomChoice(), 
            Grofman(), Shubik(), GrimTrigger(), Davis(),
            Joss(), Tullock(), Anklebreaker(), Adapter(),
            TitForTwoTats()]
        
        #Used to add strategies to the tournament using
        #the PROTOTYPE design pattern.
        self.strategy_creator = {}
        for strategy in self.basic_list_of_strategies:
            self.strategy_creator[strategy.name()] = strategy


    #Fills the tournament with the basic strategies.
    #This is called when the "Fill with basic strategies" button is pressed in the GUI.
    def fill_with_basic_strategies(self, COI):
        for strat in self.basic_list_of_strategies:
            self.add_strategy(strat.name(), COI)

    
    #Plays the tournament.
    #This is called when the "Play tournament" button is pressed in the GUI.
    def play_tournament(self):
        self.tournament.reset()
        self.tournament.play_basic_tournament()
        self.analisys.set_strategy_score_data(self.tournament.strategy_scores)
        self.analisys.set_tournament_history_data(self.tournament.tournament_history)
        self.analisys.set_matchup_move_history_data(self.tournament.strategy_move_history)
        self.analisys.set_result_matrix(self.tournament.strategy_matches)


    #Calls suitable Analisys method.
    #Called when "Table of averages" button is pressed in the GUI.
    def table_of_averages(self, ordering):
        return self.analisys.create_table_of_averages(ordering)
    

    #Calls suitable Analisys method.
    #Called when "History table" button is pressed in the GUI.
    def history_table(self):
        return self.analisys.create_history_table()
    

    #Calls suitable Analisys method.
    #Called when "Strategy history table" button is pressed in the GUI.
    def strategy_history_table(self, search):
        return self.analisys.create_strategy_history_table(search)
    

    #Calls suitable Analisys method.
    #Called when "Show moves" button is pressed in the GUI.
    def show_moves_table(self, strategy1, strategy2):
        return self.analisys.create_show_moves_table(strategy1, strategy2)
    

    #Calls suitable Analisys method.
    #Called when "Result matrix" button is pressed in the GUI.
    def result_matrix(self):
        return self.analisys.create_result_matrix()

    #Used to clear the tournament and analisys by creating new class instances.
    def clear(self):
        self.tournament = Tournament()
        self.analisys = Analisys()

    #Adds a strategy to the tournament, but also gives the strategy
    #an appropriate name by checking if a strategy of the same class
    #and the same COI is already in the tournament.
    def add_strategy(self, name, COI):
        strategy = copy.copy(self.strategy_creator[name])
        strategy.set_COI(int(COI))
        #check if there are two of the same (strategy, COI) combination
        list_of_current_names = [s.name() for s in self.tournament.list_of_strategies]
        if strategy.name() in list_of_current_names:
            self.name_strategy(strategy)
        self.tournament.add_strategy(strategy)
        return(strategy)
    
    
    #Provides a suitable name for a strategy.
    #Only called if a strategy of the same class
    #and the same COI is already in the tournament.
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
    

    #Removes strategy from the tournament
    def remove_strategy_from_tournament(self, name):
        for strategy in self.tournament.list_of_strategies:
            if strategy.name() == name:
                self.tournament.list_of_strategies.remove(strategy)
                return True
        return False
    

    #Sets the iterations of the tournament.
    #Also checks that the input is an integer n where 1 <= n <= 10000.
    #Returns True and False for testing.
    def set_iterations(self, input):
        if str(input).isnumeric():
            if int(input) >= 1 and int(input) <= 10000:
                self.tournament.set_iterations(int(input))
                return True
        return False
 