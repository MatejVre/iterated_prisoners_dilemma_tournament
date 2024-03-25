from tabulate import tabulate
import pandas as pd
from src.Model.Errors import DataError

#When creating the tables, the website on the link bellow was followed
#https://www.geeksforgeeks.org/how-to-make-a-table-in-python/

class Analisys:


    def __init__(self, tournament_history_data=None, strategy_score_data=None, matchup_move_history_data=None, result_matrix=None):
        self.__tournament_history_data = tournament_history_data
        self.__strategy_score_data = strategy_score_data
        self.__matchup_move_history_data = matchup_move_history_data
        self.__result_matrix = result_matrix


    def set_tournament_history_data(self, tournament_history_data):
        self.__tournament_history_data = tournament_history_data


    def set_strategy_score_data(self, strategy_score_data):
        self.__strategy_score_data = strategy_score_data


    def set_matchup_move_history_data(self, matchup_move_history_data):
        self.__matchup_move_history_data = matchup_move_history_data


    def set_result_matrix(self, result_matrix):
        self.__result_matrix = result_matrix


    #Method returning a tabulated history table and its corresponding dataframe
    #Corresponds to the "History table" button in the GUI
    def create_history_table(self):
        head = ["Strategy1", "Strategy2", "Strategy1", "Strategy 2"]
        data_for_table = []
        if self.__tournament_history_data == None:
            raise DataError("Data missing!")
        else:
            data_for_table = self.shape_data_for_history_table()
        history_data_frame = pd.DataFrame(data_for_table, columns=head)
        return(tabulate(data_for_table, headers=head, tablefmt="grid"), history_data_frame)
    

    #Method for shaping the data for the history table
    def shape_data_for_history_table(self):
        t_hist_data = self.__tournament_history_data
        data_for_table = []
        for game in t_hist_data.keys():
                d = []
                strategies = [game[0], game[1]]
                s = t_hist_data[game]
                score = [s[0], s[1]]
                for strat in strategies:
                    d.append(strat)
                for s in score:
                    d.append(s)
                data_for_table.append(d)
        return data_for_table

    
    #Method returning a tabulated table of averages and its corresponding dataframe
    #Corresponds to the "Table of averages" button in the GUI
    def create_table_of_averages(self, ordering):
        head = ["Strategy", "Average Score"]
        data_for_table = []
        if self.__strategy_score_data == None:
            raise DataError("Data missing!")
        else:
            data_for_table = self.shape_data_for_table_of_averages(self.__strategy_score_data)
        #sort based on the second element in the array
        data_for_table = sorted(data_for_table, key=lambda x: x[ordering], reverse=True)
        averages_frame = pd.DataFrame(data_for_table, columns=head)
        averages_frame.sort_values(by=["Strategy"], ascending=False)
        return(tabulate(data_for_table, headers=head, tablefmt="grid"), averages_frame)
    

    #Method for shaping the data for the table of averages
    def shape_data_for_table_of_averages(self, strategy_score_data):
        data_for_table = []
        number_of_strategies = len(strategy_score_data.keys())
        for strategy in self.__strategy_score_data.keys():
            d = []
            d.append(strategy)
            score = self.__strategy_score_data[strategy]//number_of_strategies
            d.append(score)
            data_for_table.append(d)
        return data_for_table


    #Method returning a tabulated strategy history and its corresponding dataframe
    #Corresponds to the "Strategy history table" button in the GUI
    #This button is used in tandem with the Strategy name text entry field
    def create_strategy_history_table(self, strategy_name: str):
        head = ["Strategy1", "Strategy2", "Strategy1", "Strategy 2"]
        data_for_table = []
        strategy_history = self.get_strategy_history(strategy_name)
        if strategy_history == None:
            raise DataError("This strategy doesn't exist. Please check spelling!")
        else:
            data_for_table = self.create_data_for_strategy_history_table( strategy_name)
        strategy_history_frame = pd.DataFrame(data_for_table, columns=head)
        return(tabulate(data_for_table, headers=head, tablefmt="grid"), strategy_history_frame)
    

    #Method used to query the tournament history data
    def get_strategy_history(self, strategy_name: str):
            strategy_history = {}
            if self.__tournament_history_data == None:
                raise DataError("Data missing!")
            for key in self.__tournament_history_data.keys():
                if strategy_name in key:
                    strategy_history[key] = self.__tournament_history_data[key]
            if len(strategy_history) == 0:
                raise DataError("This strategy doesn't exist. Please check spelling!!!")
            return strategy_history


    #Method for shaping the data for the strategy history table
    def create_data_for_strategy_history_table(self, strategy_name):
        data_for_table = []
        strategy_history = self.get_strategy_history(strategy_name)
        for game in strategy_history.keys():
                d = []
                if game[0] == strategy_name:
                    strategies = [game[0], game[1]]
                    s = strategy_history[game]
                    score = [s[0], s[1]]
                else:
                    strategies = [game[1], game[0]]
                    s = strategy_history[game]
                    score = [s[1], s[0]]
                for str in strategies:
                    d.append(str)
                for s in score:
                    d.append(s)
                data_for_table.append(d)
        return data_for_table
    

    #Method returning a tabulated result matrix and its corresponding dataframe
    #Corresponds to the "Result matrix" button in the GUI
    def create_result_matrix(self):
        data_for_table, head = self.shape_data_for_result_matrix()
        table_of_truth_frame = pd.DataFrame(data_for_table, columns=head)
        return(tabulate(data_for_table, headers=head, tablefmt="grid"), table_of_truth_frame)


    #Method for shaping the data for the result matrix
    def shape_data_for_result_matrix(self):
        if self.__result_matrix == None:
            raise DataError("Data missing!")
        else:
            head = ["Strategy"] + [x for x in self.__result_matrix.keys()] + ["Score"]
            data_for_table = []
            for key, value in self.__result_matrix.items():
                d = [0] * (len(self.__result_matrix.keys()) + 1)
                d.insert(0, key)
                running_sum = 0
                for strat, score in value.items():
                    index = head.index(strat)
                    d[index] = score
                    running_sum += score
                d[-1] = running_sum // len(self.__result_matrix.keys())
                data_for_table.append(d)
            return data_for_table, head

    
    #Method returning a tabulated show moves table and its corresponding dataframe
    #Corresponds to the "Show moves" button in the GUI
    #Used in tandem with the two drop-down menus
    def create_show_moves_table(self, strategy1_name, strategy2_name):
        head = ["move", strategy1_name, strategy2_name]
        data_for_table, data_for_pandas = self.shape_data_for_show_moves_table(strategy1_name, strategy2_name)
        pd.set_option("display.max_rows", 10000)
        matchup_move_history_frame = pd.DataFrame(data_for_pandas, columns=head[1:])
        return(tabulate(data_for_table, headers=head, tablefmt="grid"), matchup_move_history_frame)
        
        
    #Method for shaping the data for the show moves table
    def shape_data_for_show_moves_table(self, strategy1_name, strategy2_name):
        data_for_table = []
        data_for_pandas = []
        data = self.__matchup_move_history_data
        if data == None:
            raise DataError("Data missing!")
        try:
            if strategy1_name == strategy2_name:
                s1_moves = data[strategy1_name][strategy2_name][0]
                s2_moves = data[strategy1_name][strategy2_name][1]
            else:
                s1_moves = data[strategy1_name][strategy2_name]
                s2_moves = data[strategy2_name][strategy1_name]
            for i in range(len(s1_moves)):
                dft = [i, s1_moves[i], s2_moves[i]]
                data_for_table.append(dft)
                data_for_pandas.append(dft[1:])
            return data_for_table, data_for_pandas    
        except KeyError:
            raise DataError("Strategy combination not available!")
