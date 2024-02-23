from tabulate import tabulate
import pandas as pd
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


    def create_history_table(self):
        head = ["Strategy1 vs Strategy2", "Strategy1 | Strategy 2"]
        data_for_table = []
        if self.__tournament_history_data == None:
            return ("Data missing", None)
        else:
            t_hist_data = self.__tournament_history_data
            for game in t_hist_data.keys():
                d = []
                strategies = f"{game[0]} vs {game[1]}"
                s = t_hist_data[game]
                score = f"{s[0]} | {s[1]}"
                d.append(strategies)
                d.append(score)
                data_for_table.append(d)
        history_data_frame = pd.DataFrame(data_for_table, columns=head)
        return(tabulate(data_for_table, headers=head, tablefmt="grid"), history_data_frame)

    
    #https://www.geeksforgeeks.org/how-to-make-a-table-in-python/
    def create_table_of_averages(self):
        head = ["Strategy", "Average Score"]
        strategies = []
        scores = []
        data_for_table = []
        if self.__strategy_score_data == None:
            return ("Data missing", None)
        else:
            number_of_strategies = len(self.__strategy_score_data.keys())
            for strategy in self.__strategy_score_data.keys():
                d = []
                d.append(strategy)
                score = self.__strategy_score_data[strategy]//number_of_strategies
                d.append(score)
                data_for_table.append(d)
        data_for_table = sorted(data_for_table, key=lambda x: x[1], reverse=True)
        averages_frame = pd.DataFrame(data_for_table, columns=head)
        averages_frame.sort_values(by=["Strategy"], ascending=False)
        return(tabulate(data_for_table, headers=head, tablefmt="grid"), averages_frame)


    #test
    def get_strategy_history(self, strategy_name: str):
        strategy_history = {}
        for key in self.__tournament_history_data.keys():
            if strategy_name in key:
                strategy_history[key] = self.__tournament_history_data[key]
        if len(strategy_history) == 0:
            print("This strategy doesn't exist. Please check spelling!!!")
            return None
        return strategy_history
    

    def create_strategy_history_table(self, strategy_name: str):
        head = ["Strategy1 vs Strategy2", "Strategy1 | Strategy 2"]
        data_for_table = []
        strategy_history = self.get_strategy_history(strategy_name)
        if strategy_history == None:
            return "This strategy doesn't exist. Please check spelling!", None
        else:
            for game in strategy_history.keys():
                d = []
                strategies = f"{game[0]} vs {game[1]}"
                s = strategy_history[game]
                score = f"{s[0]} | {s[1]}"
                d.append(strategies)
                d.append(score)
                data_for_table.append(d)
        strategy_history_frame = pd.DataFrame(data_for_table, columns=head)
        return(tabulate(data_for_table, headers=head, tablefmt="grid"), strategy_history_frame)  