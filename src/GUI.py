import customtkinter
from Controller import Controller

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
        self.COI_input = customtkinter.CTkEntry(self, placeholder_text="0")
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
        elif str(COI).isnumeric() and int(COI) >= 0 and int(COI) <=100:
            #master.update_main_textbox("valid")
            master.controller.add_strategy(strategy_name, COI)
            master.custom_management_frame.update(master)
        else:
            master.update_main_textbox("Chance of inverse must be an integer between 0 and 100")


class ManagementFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        #fill with basic strategies
        self.fill_with_basic_strategies_button = customtkinter.CTkButton(self, text="Fill with basic strategies", command= lambda : self.fill_with_basic_strategies(master))
        self.fill_with_basic_strategies_button.grid(row=0, column=1, padx=10, pady=10,)

        #input the number of rounds
        self.tournament_rounds_input = customtkinter.CTkEntry(self, placeholder_text="number of rounds")
        self.tournament_rounds_input.grid(row=1, column = 0, padx=10, pady=10)

        #create tournament from filled strategies
        self.create_tournament_button = customtkinter.CTkButton(self, text="Create tournament", command= lambda : self.create_tournament(master))
        self.create_tournament_button.grid(row=1, column=1, padx=10, pady=10)

        #run tournament
        self.run_tournament_button = customtkinter.CTkButton(self, text="Run Tournament", command= lambda : self.run_tournament(master))
        self.run_tournament_button.grid(row=2, column=1, padx=10, pady=10,)

        #clear all
        self.clear_button = customtkinter.CTkButton(self, text="Clear all", command= lambda : self.clear_all(master))
        self.clear_button.grid(row=1, column=3)

    def fill_with_basic_strategies(self, master):
        master.controller.fill_with_basic_strategies()
        master.custom_management_frame.update(master)

    def create_tournament(self, master):
        input = self.tournament_rounds_input.get()
        if len(master.controller.custom_list_of_strategies) < 2:
            master.update_main_textbox("Not enough strategies for a tournament, please add more!")
        elif input == "":
            master.controller.create_tournament(200)
            master.update_main_textbox("Tournament with 200 rounds was created!")
        elif str(input).isnumeric():
            if int(input) >= 1:
                master.controller.create_tournament(int(input))
                master.update_main_textbox(f"Tournament with {input} rounds was created!")
        else:
            master.update_main_textbox("Number of rounds must be a number of 1 or higher")
        master.custom_management_frame.update(master)

    def run_tournament(self, master):
        if master.controller.tournament != None:
            master.controller.play_tournament()
            master.update_main_textbox("Ran tournament")
        else:
            master.update_main_textbox("Tournament not created yet! Please create the tournament first!")

    def clear_all(self, master):
        master.controller.clear()
        master.custom_management_frame.update(master)
    
    

class AnalisysFrame(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

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

    def show_table_of_averages(self, master):
        table = master.controller.analisys.create_table_of_averages()
        master.update_main_textbox(table)
    
    def show_history_table(self, master):
        table = master.controller.analisys.create_history_table()
        master.update_main_textbox(table)

    def show_strategy_history_table(self, master):
        search = self.strategy_input_box.get()
        table = master.controller.analisys.create_strategy_history_table(search)
        master.update_main_textbox(table)
        

class CustomManagementFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)


    def update(self, master):
        for child in self.winfo_children():
            child.destroy()
        for i, strategy in enumerate(master.controller.custom_list_of_strategies):
            self.label = customtkinter.CTkLabel(self, text=strategy.name())
            self.label.grid(row=i//2, column=(i)%2, pady=2, padx=10)
            if master.controller.tournament and strategy in master.controller.tournament.list_of_strategies:
                (self.label.configure(text_color="green"))
            

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
        
    def update_main_textbox(self, value):
        self.main_textbox.configure(state="normal")
        self.main_textbox.delete("0.0", "end")
        self.main_textbox.insert(customtkinter.END, value)
        self.main_textbox.configure(state="disabled")

app = App()
app.mainloop()