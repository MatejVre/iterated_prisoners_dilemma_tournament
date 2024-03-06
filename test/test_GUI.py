import pytest
import randtest
import random
from src.Model.Strategies import *
from src.Model.Game import Game
from src.Model.Tournament import Tournament
from src.Controller.Controller import *
from src.Model.Errors import TournamentSizeError
from src.View.GUI import App

class Test_GUI_Functions():
    
    def test_COI_valid(self):
        app = App()
        COI = -1
        assert app.COI_valid(COI) == False
        COI = 0
        assert app.COI_valid(COI) == True
        COI = 1
        assert app.COI_valid(COI) == True
        COI = 99
        assert app.COI_valid(COI) == True
        COI = 100
        assert app.COI_valid(COI) == True
        COI = 101
        assert app.COI_valid(COI) == False
        COI = "i am a random string"
        assert app.COI_valid(COI) == False