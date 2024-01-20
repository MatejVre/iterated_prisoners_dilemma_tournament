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

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.controller.create_basic_tournament()
        self.controller.play_tournament()
        self.title("Iterated Prisoners Dilemma Tournament")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.main_textbox = customtkinter.CTkTextbox(self, height=780, width=580, state="disabled", font=customtkinter.CTkFont("terminal", 16))
        self.main_textbox.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.grid_columnconfigure(1, weight=1)

        self.display_table_of_averages = customtkinter.CTkButton(self, text="Table of averages", command=self.show_table_of_averages)
        self.display_table_of_averages.grid(row=0, column=0)
        #self.management_frame = ManagementFrame(self)
        #self.management_frame.grid(row=0, column=0)

    def show_table_of_averages(self):
        self.main_textbox.configure(state="normal")
        table = self.controller.analisys.create_table_of_averages()
        print(table)
        self.main_textbox.insert(customtkinter.END, table)
        self.main_textbox.configure(state="disabled")

        
    

        

app = App()
app.mainloop()