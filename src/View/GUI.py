from PIL import Image
import customtkinter
from pandas import DataFrame
from Controller.Controller import *
from View.AdditionFrame import StrategyAddittionFrame
from View.TournamentManagementFrame import TournamentManagementFrame
from View.AnalisysFrame import AnalisysFrame
from View.StrategyInformationFrame import StrategyInformationFrame



class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.title("Iterated Prisoners Dilemma Tournament")
        self.geometry("1200x800")
        customtkinter.set_appearance_mode("dark")
        self.resizable(False, False)
        self.main_textbox = customtkinter.CTkTextbox(self, state="disabled", font=customtkinter.CTkFont("Monaco", 14))
        self.main_textbox.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nesw")
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.strategy_addition_frame = StrategyAddittionFrame(self)
        self.strategy_addition_frame .grid(row=0, column=0)

        self.tournament_management_frame = TournamentManagementFrame(self)
        self.tournament_management_frame.grid(row=1, column=0)

        self.custom_management_frame = StrategyInformationFrame(self)
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