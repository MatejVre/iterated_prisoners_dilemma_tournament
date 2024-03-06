import customtkinter


class StrategyAddittionFrame(customtkinter.CTkFrame):
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
        COI = self.COI_input.get()
        if COI == "":
            master.controller.add_strategy(strategy_name, 0)
            master.custom_management_frame.update(master)
        elif master.COI_valid(COI):
            master.controller.add_strategy(strategy_name, COI)
            master.custom_management_frame.update(master)
        else:
            master.update_main_textbox("Chance of inverse must be an integer between 0 and 100")