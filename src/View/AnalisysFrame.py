import customtkinter
from src.Model.Errors import DataError

class AnalisysFrame(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.clipboard_dataframe = None

        self.checkbox = customtkinter.CTkCheckBox(self, text="Order by scores")
        self.checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        #table of averages button
        self.display_table_of_averages_button = customtkinter.CTkButton(self, text="Table of averages", command= lambda : self.show_table_of_averages(master))
        self.display_table_of_averages_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        #history table button
        self.display_history_table_button = customtkinter.CTkButton(self, text="History table", command= lambda : self.show_history_table(master))
        self.display_history_table_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        #strategy history table input box
        self.strategy_input_box = customtkinter.CTkEntry(self, placeholder_text="Strategy name")
        self.strategy_input_box.grid(row=1, column=0)

        #strategy history table button
        self.display_strategy_history_table_button = customtkinter.CTkButton(self, text="Strategy history table", command= lambda : self.show_strategy_history_table(master))
        self.display_strategy_history_table_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        #table of truth
        self.table_of_truth_button = customtkinter.CTkButton(self, text="Result matrix", command= lambda : self.show_the_table(master))
        self.table_of_truth_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        #strategy selector 1
        self.strategy_selection_menu1 = customtkinter.CTkOptionMenu(self, values=["None"], state="disabled")
        self.strategy_selection_menu1.grid(row=2, column=0, pady=10, padx=10)

        #strategy selector 2
        self.strategy_selection_menu2 = customtkinter.CTkOptionMenu(self, values=["None"], state="disabled")
        self.strategy_selection_menu2.grid(row=2, column=1, pady=10, padx=10)

        #show moves button
        self.show_moves_button = customtkinter.CTkButton(self, text="Show moves", command= lambda : self.show_strategy_moves(master))
        self.show_moves_button.grid(row=2, column=2, pady=10, padx=10)


#Analisys functions return a tuple. The first element is the table stylized for the user, and the second one is the
#Pandas dataframe with the same data as the first element (used for copying to clipboard)


    def show_table_of_averages(self, master):
        try:
            result = master.controller.table_of_averages(self.checkbox.get())
            table = result[0]
            self.clipboard_dataframe = result[1]
            master.update_main_textbox(table)
            master.update_clipboard_button()
        except DataError as e:
            master.update_main_textbox(e)
            master.update_clipboard_button()
    
    def show_history_table(self, master):
        try:
            result = master.controller.history_table()
            table = result[0]
            self.clipboard_dataframe = result[1]
            master.update_main_textbox(table)
            master.update_clipboard_button()
        except DataError as e:
            master.update_main_textbox(e)
            master.update_clipboard_button()


    def show_strategy_history_table(self, master):
        try:
            search = self.strategy_input_box.get()
            result = master.controller.strategy_history_table(search)
            table = result[0]
            self.clipboard_dataframe = result[1]
            master.update_main_textbox(table)
            master.update_clipboard_button()
        except DataError as e:
            master.update_main_textbox(e)
            master.update_clipboard_button()
    
    def show_strategy_moves(self, master):
        strategy1 = self.strategy_selection_menu1.get()
        strategy2 = self.strategy_selection_menu2.get()
        try:
            result = master.controller.matchup_move_history_table(strategy1, strategy2)
            table = result[0]
            self.clipboard_dataframe = result[1]
            master.update_main_textbox(table)
            master.update_clipboard_button()
        except (DataError, KeyError) as e:
            master.update_main_textbox(e)
            master.update_clipboard_button()

    def show_the_table(self, master):
        try:
            result = master.controller.analisys.create_matchup_matrix()
            table = result[0]
            self.clipboard_dataframe = result[1]
            master.update_main_textbox(table)
            master.update_clipboard_button()
        except (DataError) as e:
            master.update_main_textbox(e)
            master.update_clipboard_button()

    #Used to update the bottom most dropdown menus of the analisys frame based on the
    #strategies that are currently in the tournament.
    def update_strategy_selectors(self, master):
        strat_list = master.controller.tournament.strategy_move_history.keys()
        print(strat_list)
        if strat_list != []:
            self.strategy_selection_menu1.configure(values=[x for x in strat_list], state="normal")
            self.strategy_selection_menu2.configure(values=[x for x in strat_list], state="normal")
        else:
            self.strategy_selection_menu2.configure(values=["None"], state="disabled")
            self.strategy_selection_menu1.configure(values=["None"], state="disabled")