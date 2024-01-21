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
            self.addButton = customtkinter.CTkButton(self, text="Add strategy", command=self.open_strategy_adder)
            self.addButton.grid(row=0, column=0, padx=10, pady=10)
            self.createTournamentButton = customtkinter.CTkButton(self, text="Create tournament")
            self.createTournamentButton.grid(row=1, column=0, padx=10, pady=10)
            self.clearButton = customtkinter.CTkButton(self, text="Clear")
            self.clearButton.grid(row=2, column=0, padx=10, pady=10)
            self.strategy_adder = None

        def open_strategy_adder(self):
            if self.strategy_adder == None or not self.strategy_adder.winfo_exists():
                self.strategy_adder = StrategyAdder(self)
            else:
                self.strategy_adder.focus()

class AnalisysFrame(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        #table of averages button
        self.display_table_of_averages = customtkinter.CTkButton(self, text="Table of averages", command= lambda : self.show_table_of_averages(master))
        self.display_table_of_averages.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        #history table button
        self.display_history_table = customtkinter.CTkButton(self, text="History table", command= lambda : self.show_history_table(master))
        self.display_history_table.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        #strategy history table input box
        self.strategy_input_box = customtkinter.CTkEntry(self, placeholder_text="Strategy name")
        self.strategy_input_box.grid(row=1, column=0)

        #strategy history table button
        self.display_strategy_history_table = customtkinter.CTkButton(self, text="Strategy table", command= lambda : self.show_strategy_history_table(master))
        self.display_strategy_history_table.grid(row=1, column=1, padx=10, pady=10, sticky="w")



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
        


class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.controller.create_basic_tournament()
        self.controller.play_tournament()
        self.title("Iterated Prisoners Dilemma Tournament")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.main_textbox = customtkinter.CTkTextbox(self, height=780, width=580, state="disabled", font=customtkinter.CTkFont("terminal", 14))
        self.main_textbox.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.analisys_frame = AnalisysFrame(self)
        self.analisys_frame.grid(row=0, column=0)
        
        #self.management_frame = ManagementFrame(self)
        #self.management_frame.grid(row=0, column=0)

    def update_main_textbox(self, value):
        self.main_textbox.configure(state="normal")
        self.main_textbox.delete("0.0", "end")
        self.main_textbox.insert(customtkinter.END, value)
        self.main_textbox.configure(state="disabled")
    

        
    

        

app = App()
app.mainloop()