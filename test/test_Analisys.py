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
        analisys = Analisys()
        games = t.tournament_history
        analisys.set_tournament_history_data(games)
        data_to_test = analisys.create_data_for_history_table()
        for game, scores in games.values():
            assert [game[0], game[1], scores[0], scores[1]] in data_to_test

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
            analisys.create_table_of_averages(0)
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
        t.play_basic_tournament()
        with pytest.raises(DataError) as excinfo:
            analisys.get_strategy_history("i deffinitely don't exist but it doesn't matter because the data is empty anyways")
        assert str(excinfo.value) == "Data missing!"
        history = t.tournament_history
        analisys.set_tournament_history_data(history)
        with pytest.raises(DataError) as excinfo:
            analisys.get_strategy_history("i deffinitely don't exist")
        assert str(excinfo.value) == "This strategy doesn't exist. Please check spelling!!!"

    def test_create_data_for_strategy_history_table(self):
        t = self.setup_method()
        analisys = Analisys()
        t.play_basic_tournament()
        analisys.set_matchup_move_history_data(t.strategy_move_history)
        with pytest.raises(DataError) as excinfo:
            analisys.create_data_for_matchup_move_history_table("TitForTat", "This strategy deffinitely doesn't exist")
        assert str(excinfo.value) == "strategy combination not available!"
        with pytest.raises(DataError) as excinfo:
            analisys.create_data_for_matchup_move_history_table("This strategy deffinitely doesn't exist", "TitForTat")
        assert str(excinfo.value) == "strategy combination not available!"
        data = analisys.create_data_for_matchup_move_history_table("TitForTat", "TitForTat")
        for row in data[0]:
            assert row[1:] == [0, 0]
        data = analisys.create_data_for_matchup_move_history_table("TitForTat", "AlwaysDefect")
        assert data[0][0][1:] == [0, 1]
        for row in data[0][1:]:
            assert row[1:] == [1, 1]
