import customtkinter
from Controller import Controller

class StrategyAdder(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200+600+400")
        self.label = customtkinter.CTkLabel(self, text="Hi there!")
        self.label.pack()

class ManagementFrame(customtkinter.CTkFrame):
        def __init__(self, master):
            super().__init__(master)
            
            #fill with basic strategies
            self.fill_with_basic_strategies_button = customtkinter.CTkButton(self, text="Fill with basic strategies", command= lambda : self.fill_with_basic_strategies(master))
            self.fill_with_basic_strategies_button.grid(row=0, column=0, padx=10, pady=10,)

            #create tournament from filled strategies
            self.create_tournament_button = customtkinter.CTkButton(self, text="Create tournament", command= lambda : self.create_tournament(master))
            self.create_tournament_button.grid(row=1, column=0, padx=10, pady=10)

            #run tournament
            self.run_tournament_button = customtkinter.CTkButton(self, text="Run Tournament", command= lambda : self.run_tournament(master))
            self.run_tournament_button.grid(row=2, column=0, padx=10, pady=10,)

        def fill_with_basic_strategies(self, master):
            master.controller.fill_with_basic_strategies()
            master.custom_management_frame.update(master)

        def create_tournament(self, master):
            if master.controller.custom_list_of_strategies != []:
                master.controller.create_tournament(200)
                master.update_main_textbox("Tournament was created!")
            else:
                master.update_main_textbox("Not enough strategies for a tournament, please add more!")

        def run_tournament(self, master):
            if master.controller.tournament != None:
                master.controller.play_tournament()
                master.update_main_textbox("Ran tournament")
            else:
                master.update_main_textbox("Tournament not created yet! Please create the tournament first!")

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
        for i, strategy in enumerate(master.controller.custom_list_of_strategies):
            self.label = customtkinter.CTkLabel(self, text=strategy.name())
            self.label.grid(row=i//2, column=(i+1)%2, pady=2, padx=10)
            

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.title("Iterated Prisoners Dilemma Tournament")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.main_textbox = customtkinter.CTkTextbox(self, state="disabled", font=customtkinter.CTkFont("terminal", 14))
        self.main_textbox.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nesw")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.management_frame = ManagementFrame(self)
        self.management_frame.grid(row=0, column=0)

        self.custom_management_frame = CustomManagementFrame(self)
        self.custom_management_frame.grid(row=1, column=0, sticky="ew")
        
        self.analisys_frame = AnalisysFrame(self)
        self.analisys_frame.grid(row=2, column=0)
        
        

    def update_main_textbox(self, value):
        self.main_textbox.configure(state="normal")
        self.main_textbox.delete("0.0", "end")
        self.main_textbox.insert(customtkinter.END, value)
        self.main_textbox.configure(state="disabled")
    

        
    

        

app = App()
app.mainloop()