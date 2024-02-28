from PIL import Image
import customtkinter
from pandas import DataFrame
from Controller import *

class StrategyAdder(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200+600+400")
        self.label = customtkinter.CTkLabel(self, text="Hi there!")
        self.label.pack()


class AddittionFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        #strategy dropdown menu
        self.strategy_dropdown_menu = customtkinter.CTkOptionMenu(self, values=[x.name() for x in master.controller.basic_list_of_strategies])
        self.strategy_dropdown_menu.grid(row=0, column=0, pady=10, padx=10)
 
        #COI input field
        self.COI_input = customtkinter.CTkEntry(self, placeholder_text="COI")
        self.COI_input.grid(row=0, column=1, pady=10, padx=10)

        #add button
        self.add_button = customtkinter.CTkButton(self, text="Add", command= lambda : self.add_strategy(master))
        self.add_button.grid(row=0, column=2, pady=10, padx=10)

    def add_strategy(self, master):
        strategy_name = self.strategy_dropdown_menu.get()
        #master.update_main_textbox(strategy_name)
        COI = self.COI_input.get()
        if COI == "":
            #master.update_main_textbox("valid")
            master.controller.add_strategy(strategy_name, 0)
            master.custom_management_frame.update(master)
        elif master.COI_valid(COI):
            #master.update_main_textbox("valid")
            master.controller.add_strategy(strategy_name, COI)
            master.custom_management_frame.update(master)
        else:
            master.update_main_textbox("Chance of inverse must be an integer between 0 and 100")


class ManagementFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        #Set coi for fill with basic strategies
        self.COI_for_fill = customtkinter.CTkEntry(self, placeholder_text="COI")
        self.COI_for_fill.grid(row=0, column=0, padx=10, pady=10)

        #fill with basic strategies
        self.fill_with_basic_strategies_button = customtkinter.CTkButton(self, text="Fill with basic strategies", command= lambda : self.fill_with_basic_strategies(master))
        self.fill_with_basic_strategies_button.grid(row=0, column=1, padx=10, pady=10)

        #input the number of rounds
        self.tournament_rounds_input = customtkinter.CTkEntry(self, placeholder_text="number of rounds")
        self.tournament_rounds_input.grid(row=1, column = 0, padx=10, pady=10)

        #create tournament from filled strategies
        self.set_rounds_button = customtkinter.CTkButton(self, text="Set rounds", command= lambda : self.set_rounds(master))
        self.set_rounds_button.grid(row=1, column=1, padx=10, pady=10)

        #run tournament
        self.run_tournament_button = customtkinter.CTkButton(self, text="Run Tournament", command= lambda : self.run_tournament(master))
        self.run_tournament_button.grid(row=2, column=1, padx=10, pady=10,)

        #clear all
        self.clear_button = customtkinter.CTkButton(self, text="Clear all", command= lambda : self.clear_all(master))
        self.clear_button.grid(row=1, column=3)

    def fill_with_basic_strategies(self, master):
        COI = self.COI_for_fill.get()
        if COI == "":
            #master.update_main_textbox("valid")
            master.controller.fill_with_basic_strategies(0)
            master.custom_management_frame.update(master)
        elif master.COI_valid(COI):
            #master.update_main_textbox("valid")
            master.controller.fill_with_basic_strategies(COI)
            master.custom_management_frame.update(master)
        else:
            master.update_main_textbox("Chance of inverse must be an integer between 0 and 100")

    def set_rounds(self, master):
        input = self.tournament_rounds_input.get()
        if str(input).isnumeric():
            if int(input) >= 1:
                master.controller.set_tournament_iterations(int(input))
                master.update_main_textbox(f"Tournament with {input} rounds was created!")
        else:
            master.update_main_textbox("Number of rounds must be a number of 1 or higher")
        master.custom_management_frame.update(master)

    def run_tournament(self, master):
        try:
            master.controller.play_tournament()
            master.update_main_textbox(f"Ran tournament with {master.controller.tournament.iterations} rounds")
            master.analisys_frame.update_strategy_selectors(master)
        except TournamentSizeError as e:
            master.update_main_textbox(e)

    def clear_all(self, master):
        master.controller.clear()
        master.custom_management_frame.update(master)
        master.analisys_frame.clipboard_dataframe = None
        master.update_main_textbox("")
        master.update_clipboard_button()
        master.analisys_frame.update_strategy_selectors(master)
    
    

class AnalisysFrame(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.clipboard_dataframe = None

        #table of averages button
        self.display_table_of_averages_button = customtkinter.CTkButton(self, text="Table of averages", command= lambda : self.show_table_of_averages(master))
        self.display_table_of_averages_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        #history table button
        self.display_history_table_button = customtkinter.CTkButton(self, text="History table", command= lambda : self.show_history_table(master))
        self.display_history_table_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        #strategy history table input box
        self.strategy_input_box = customtkinter.CTkEntry(self, placeholder_text="Strategy name")
        self.strategy_input_box.grid(row=1, column=0)

        #strategy history table button
        self.display_strategy_history_table_button = customtkinter.CTkButton(self, text="Strategy table", command= lambda : self.show_strategy_history_table(master))
        self.display_strategy_history_table_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        #strategy selector 1
        self.strategy_selection_menu1 = customtkinter.CTkOptionMenu(self, values=["None"], state="disabled")
        self.strategy_selection_menu1.grid(row=2, column=0, pady=10, padx=10)

        #strategy selector 2
        self.strategy_selection_menu2 = customtkinter.CTkOptionMenu(self, values=["None"], state="disabled")
        self.strategy_selection_menu2.grid(row=2, column=1, pady=10, padx=10)

        #show moves button
        self.show_moves_button = customtkinter.CTkButton(self, text="Show moves", command= lambda : self.show_strategy_moves(master))
        self.show_moves_button.grid(row=2, column=2, pady=10, padx=10)

    def show_table_of_averages(self, master):
        result = master.controller.analisys.create_table_of_averages()
        table = result[0]
        self.clipboard_dataframe = result[1]
        master.update_main_textbox(table)
        master.update_clipboard_button()
    
    def show_history_table(self, master):
        result = master.controller.analisys.create_history_table()
        table = result[0]
        self.clipboard_dataframe = result[1]
        master.update_main_textbox(table)
        master.update_clipboard_button()

    def show_strategy_history_table(self, master):
        search = self.strategy_input_box.get()
        result = master.controller.analisys.create_strategy_history_table(search) 
        table = result[0]
        self.clipboard_dataframe = result[1]
        master.update_main_textbox(table)
        master.update_clipboard_button()
    
    def show_strategy_moves(self, master):
        strategy1 = self.strategy_selection_menu1.get()
        strategy2 = self.strategy_selection_menu2.get()
        result = master.controller.analisys.create_matchup_move_history_table(strategy1, strategy2)
        table = result[0]
        self.clipboard_dataframe = result[1]
        master.update_main_textbox(table)
        master.update_clipboard_button()

    
    def update_strategy_selectors(self, master):
        strat_list = master.controller.tournament.strategy_move_history.keys()
        print(strat_list)
        if strat_list != []:
            self.strategy_selection_menu1.configure(values=[x for x in strat_list], state="normal")
            self.strategy_selection_menu2.configure(values=[x for x in strat_list], state="normal")
        else:
            self.strategy_selection_menu2.configure(values=["None"], state="disabled")
            self.strategy_selection_menu1.configure(values=["None"], state="disabled")

class CustomManagementFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.number_of_iterations = customtkinter.CTkLabel(self, text=f"Number of iterations: {master.controller.tournament.iterations}")
        self.number_of_iterations.grid(row=0, column=0, pady=2, padx=10)


    def update(self, master):
        for child in self.winfo_children():
            child.destroy()
        self.number_of_iterations = customtkinter.CTkLabel(self, text=f"Number of iterations: {master.controller.tournament.iterations}")
        self.number_of_iterations.grid(row=0, column=0, pady=2, padx=10)
        for i, strategy in enumerate(master.controller.tournament.list_of_strategies):
            self.label_button = customtkinter.CTkButton(self, text=strategy.name(), command= lambda n = strategy.name() : self.remove_strategy_from_tournament(master, n))
            self.label_button.grid(row=1 + i//3, column=(i)%3, pady=2, padx=10)

    
    def remove_strategy_from_tournament(self, master, name):
        try:
            master.controller.remove_strategy_from_tournament(name)
            self.update(master)
        except TournamentSizeError as e:
            master.update_main_textbox(e)
    
    def remove_strategy_from_queue(self, master, name):
        master.controller.remove_strategy_from_queue(name)
        self.update(master)            

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.title("Iterated Prisoners Dilemma Tournament")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.main_textbox = customtkinter.CTkTextbox(self, state="disabled", font=customtkinter.CTkFont("terminal", 14))
        self.main_textbox.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nesw")
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.addition_frame = AddittionFrame(self)
        self.addition_frame .grid(row=0, column=0)

        self.management_frame = ManagementFrame(self)
        self.management_frame.grid(row=1, column=0)

        self.custom_management_frame = CustomManagementFrame(self)
        self.custom_management_frame.grid(row=2, column=0, padx=5, pady=5, sticky="we")
        
        self.analisys_frame = AnalisysFrame(self)
        self.analisys_frame.grid(row=3, column=0, padx=5, pady=10,)

        image = customtkinter.CTkImage(dark_image=Image.open("src\\static\\clipboard.png"), size=(30, 30))
        self.copy_button = customtkinter.CTkButton(self, text="", image=image, width=30, height=30, command= self.copy_to_clipboard, state="disabled")
        self.copy_button.place(x=1125, y=20)
        
    def update_main_textbox(self, value):
        self.main_textbox.configure(state="normal")
        self.main_textbox.delete("0.0", "end")
        self.main_textbox.insert(customtkinter.END, value)
        self.main_textbox.configure(state="disabled")
    

    def copy_to_clipboard(self):
        self.analisys_frame.clipboard_dataframe.to_clipboard()
    

    def update_clipboard_button(self):
        clipboard = self.analisys_frame.clipboard_dataframe
        if not isinstance(clipboard, DataFrame):
            self.copy_button.configure(state="disabled")
        else:
            self.copy_button.configure(state="normal")

    def COI_valid(self, COI):
        return str(COI).isnumeric() and int(COI) >= 0 and int(COI) <=100