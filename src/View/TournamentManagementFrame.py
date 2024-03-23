import customtkinter
from Model.Errors import TournamentSizeError

class TournamentManagementFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        #Set COI for fill with basic strategies
        self.COI_for_fill = customtkinter.CTkEntry(self, placeholder_text="Chance of inverse")
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
            master.controller.fill_with_basic_strategies(0)
            master.custom_management_frame.update(master)
        elif master.COI_valid(COI):
            master.controller.fill_with_basic_strategies(COI)
            master.custom_management_frame.update(master)
        else:
            master.update_main_textbox("Chance of inverse must be an integer between 0 and 100")

    def set_rounds(self, master):
        input = self.tournament_rounds_input.get()
        response = master.controller.set_iterations(input)
        if response:
            master.update_main_textbox(f"Number of iterations set to {input}")
        else:
            master.update_main_textbox("Number of rounds must be an integer between 1 or 10,000")
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