import pytest
import randtest
import random
from src.Model.Strategies import *
from src.Controller.Controller import *


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
    

    def test_set_iterations(self):
        c = Controller()
        assert c.set_iterations("asdojfh") == False
        assert c.set_iterations(0) == False
        assert c.set_iterations(1) == True
        assert c.set_iterations(10000) == True
        assert c.set_iterations(10001) == False


    def test_insert_all(self):
        c = Controller()
        c.fill_with_basic_strategies(0)
        c.fill_with_basic_strategies(5)
        names = [x.name() for x in c.tournament.list_of_strategies]
        #have to match names since we cannot access the specific objects in list of strategies
        strats = [
        "TitForTat","AlwaysDefect","Shubik","Grofman","AlwaysCooperate","RandomChoice","Joss","Adapter","Anklebreaker","TitForTwoTats",
        "Tullock","Davis","GrimTrigger","TitForTat-5%","AlwaysDefect-5%","Shubik-5%","Grofman-5%","AlwaysCooperate-5%","RandomChoice-5%",
        "Joss-5%","Adapter-5%","Anklebreaker-5%","TitForTwoTats-5%","Tullock-5%","Davis-5%","GrimTrigger-5%"
        ]
        assert all(i in names for i in strats)

