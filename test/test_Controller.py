import pytest
import randtest
import random
from src.Model.Strategies import *
from src.Model.Game import Game
from src.Model.Tournament import Tournament
from src.Controller.Controller import *
from src.Model.Errors import TournamentSizeError
from src.View.GUI import App

class Test_Controller_Functions():

    def test_add_strategy(self):
        c = Controller()
        s1 = c.add_strategy("TitForTat", 1)
        s2 = c.add_strategy("TitForTat", 1)
        s3 = c.add_strategy("Joss", 0)
        assert s1 != s2
        assert s1.name() == "TitForTat-1%"
        assert s2.name() == "TitForTat-1%-1"
        assert s3.name() == "Joss"

    def test_name_strategy(self):
        c = Controller()
        c.add_strategy("TitForTat", 0)
        c.add_strategy("TitForTat", 0)
        list = [s.name() for s in c.tournament.list_of_strategies]
        assert  "TitForTat" in list
        assert "TitForTat-1" in list

    def test_remove_strategy_from_tournament(self):
        c = Controller()
        c.fill_with_basic_strategies(0)
        assert c.remove_strategy_from_tournament("TitForTat") == True
        assert c.remove_strategy_from_tournament("Random name that deffinitely does not work") == False
