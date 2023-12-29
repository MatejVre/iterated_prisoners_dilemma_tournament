from tabulate import tabulate
class Analisys:

    def __init__(self, tournament_history_data=None, strategy_score_data=None):
        self.__tournament_history_data = tournament_history_data
        self.__strategy_score_data = strategy_score_data

    def set_tournament_history_data(self, tournament_history_data):
        self.__tournament_history_data = tournament_history_data

    def set_strategy_score_data(self, strategy_score_data):
        self.__strategy_score_data = strategy_score_data

    def create_full_table(self):
        if self.__tournament_history_data == None:
            print("Data missing")
    
    #https://www.geeksforgeeks.org/how-to-make-a-table-in-python/
    def create_table_of_averages(self):
        head = ["Strategy", "Average Score"]
        data_for_table = []
        if self.__strategy_score_data == None:
            print("Data missing")
        else:
            number_of_strategies = len(self.__strategy_score_data.keys())
            for strategy in self.__strategy_score_data.keys():
                d = []
                d.append(strategy)
                d.append(self.__strategy_score_data[strategy]//number_of_strategies)
                data_for_table.append(d)
        return(tabulate(data_for_table, headers=head, tablefmt="grid"))