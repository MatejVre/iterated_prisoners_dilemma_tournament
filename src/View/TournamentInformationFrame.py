import customtkinter
from Model.Errors import TournamentSizeError

class TournamentInformationFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.number_of_iterations = customtkinter.CTkLabel(self, text=f"Number of rounds: {master.controller.tournament.iterations}")
        self.number_of_iterations.grid(row=0, column=0, pady=2, padx=10)


    def update(self, master):
        for child in self.winfo_children():
            child.destroy()
        self.number_of_iterations = customtkinter.CTkLabel(self, text=f"Number of rounds: {master.controller.tournament.iterations}")
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