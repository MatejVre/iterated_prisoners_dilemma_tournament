import pytest
import randtest
import random
from src.Model.Strategies import *
from src.Controller.Controller import *
from src.Model.Tournament import *

class Test_Analisys():

    def setup_method(self):
        t = Tournament()
        tft = TitForTat()
        ac = AlwaysCooperate()
        ad = AlwaysDefect()
        t.add_strategy(tft)
        t.add_strategy(ac)
        t.add_strategy(ad)
        return t

    #test appropriate values, known outcomes used to test this function
    def test_history_table(self):
        t = self.setup_method()
        t.play_basic_tournament()
        tournament_history = t.tournament_history
        analisys = Analisys()
        analisys.set_tournament_history_data(tournament_history)
        data = analisys.create_data_for_history_table(tournament_history)
        for key, value in tournament_history.items():
            assert [f"{key[0]} vs {key[1]}", f"{value[0]} | {value[1]}"] in data

    #https://pytest-with-eric.com/introduction/pytest-assert-exception/
    def test_history_table_error(self):
        analisys = Analisys()
        with pytest.raises(DataError) as excinfo:
            analisys.create_history_table()
        assert str(excinfo.value) == "Data missing!"

    def test_table_of_averages(self):
        t = Tournament()
        tft = TitForTat()
        ac = AlwaysCooperate()
        gf = Grofman()
        strats = [tft.name(), ac.name(), gf.name()]
        t.add_strategy(tft)
        t.add_strategy(ac)
        t.add_strategy(gf)
        t.play_basic_tournament()
        strategy_scores = t.strategy_scores
        analisys = Analisys()
        analisys.set_strategy_score_data(strategy_scores)
        data = analisys.create_data_for_table_of_averages(strategy_scores)
        assert len(data) == 3
        for row in data:
            assert row[0] in strats
            assert row[1] == 600
            #ensures uniqueness
            strats.remove(row[0])

    def test_table_of_averages_error(self):
        analisys = Analisys()
        with pytest.raises(DataError) as excinfo:
            analisys.create_table_of_averages()
        assert str(excinfo.value) == "Data missing!"

    def test_get_strategy_history(self):
        t = self.setup_method()
        analisys = Analisys()
        t.play_basic_tournament()
        history = t.tournament_history
        analisys.set_tournament_history_data(history)
        data = analisys.get_strategy_history("TitForTat")
        assert len(data) == 3
        for key, value in data.items():
            if "AlwaysDefect" in key:
                assert value == [199, 204]
            else:
                assert value == [600, 600]
                
    def test_get_strategy_history_error(self):
        t = self.setup_method()
        analisys = Analisys()
        with pytest.raises(DataError) as excinfo:
            analisys.get_strategy_history("i deffinitely don't exist but it doesn't matter because the data is empty anyways")
        assert str(excinfo.value) == "Data missing!"
        history = t.tournament_history
        analisys.set_tournament_history_data(history)
        with pytest.raises(DataError) as excinfo:
            analisys.get_strategy_history("i deffinitely don't exist")
        assert str(excinfo.value) == "This strategy doesn't exist. Please check spelling!!!"