from PIL import Image
import customtkinter
from pandas import DataFrame
from Controller.Controller import *
from View.AdditionFrame import StrategyAddittionFrame
from View.TournamentManagementFrame import TournamentManagementFrame
from View.AnalisysFrame import AnalisysFrame
from src.View.TournamentInformationFrame import TournamentInformationFrame
from pathlib import Path



class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.title("Iterated Prisoners Dilemma Tournament")
        self.geometry("1200x800")
        customtkinter.set_appearance_mode("dark")
        self.resizable(False, False)

        #configuring the grid to achieve a desired layout
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #represent the big textbox on the rightmost side of the program
        self.main_textbox = customtkinter.CTkTextbox(self, state="disabled", font=customtkinter.CTkFont("Monaco", 14), wrap="none")
        self.main_textbox.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nesw")

        #represents the frame used for adding a singular strategy and setting its COI
        self.strategy_addition_frame = StrategyAddittionFrame(self)
        self.strategy_addition_frame .grid(row=0, column=0)

        #represents the frame used for configuring the tournament, clearing, etc.
        self.tournament_management_frame = TournamentManagementFrame(self)
        self.tournament_management_frame.grid(row=1, column=0)

        #represents the frame displaying the strategies that are currently in the tournament and number of rounds
        self.custom_management_frame = TournamentInformationFrame(self)
        self.custom_management_frame.grid(row=2, column=0, padx=5, pady=5, sticky="we")
        
        #represents the frame which holds everything to do with tables and data
        self.analisys_frame = AnalisysFrame(self)
        self.analisys_frame.grid(row=3, column=0, padx=5, pady=10,)

        #this is used to create the clipboard button used to copy data tables in excel format
        image = customtkinter.CTkImage(dark_image=Image.open(Path("src/static/clipboard.png")), size=(25, 25))
        self.copy_button = customtkinter.CTkButton(self, text="", image=image, width=25, height=25, command= self.copy_to_clipboard, state="disabled")
        self.copy_button.place(x=1150, y=10)
        
    #function that is used each time the text displayed in the main textbox is changed
    def update_main_textbox(self, value):
        self.main_textbox.configure(state="normal")
        self.main_textbox.delete("0.0", "end")
        self.main_textbox.insert("1.50", "\n" + str(value))
        self.main_textbox.configure(state="disabled")
        self.update_clipboard_button()
    #copies the text to the clipboard. Only callable if the text is displaying a table
    def copy_to_clipboard(self):
        self.analisys_frame.clipboard_dataframe.to_clipboard()
    
    #makes the clipboard button active or inactive based on whether the text displayed
    #in the main textbox is a table or not
    def update_clipboard_button(self):
        clipboard = self.analisys_frame.clipboard_dataframe
        if not isinstance(clipboard, DataFrame):
            self.copy_button.configure(state="disabled")
        else:
            self.copy_button.configure(state="normal")

    #was this copied from somewhere?
    #check if chance of inverse is an integer between 0 and 100
    def COI_valid(self, COI):
        return str(COI).isnumeric() and int(COI) >= 0 and int(COI) <=100
    
    def clear_clipboard_dataframe(self):
        self.analisys_frame.clipboard_dataframe = None
        self.update_clipboard_button()