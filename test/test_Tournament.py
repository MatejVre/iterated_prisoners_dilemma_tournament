import pytest
from src.Model.Strategies import *
from src.Model.Tournament import Tournament
from src.Controller.Controller import *

class Test_Tournament():

    def test_add_strategy(self):
        shubik = Shubik()
        alwaysDefect = AlwaysDefect()
        tournament = Tournament()
        tournament.add_strategy(shubik)
        tournament.add_strategy(alwaysDefect)
        assert shubik in tournament.list_of_strategies and alwaysDefect in tournament.list_of_strategies


    def test_add_strategy_score(self):
        tournament = Tournament()
        shubik = Shubik()
        tournament.add_strategy_score(shubik, 500)
        assert tournament.strategy_scores[shubik.name()] == 500
        tournament.add_strategy_score(shubik, 500)
        assert tournament.strategy_scores[shubik.name()] == 1000
    

    def test_play_basic_tournament(self):
        tournament = Tournament()
        alwaysCooperate = AlwaysCooperate()
        titForTat = TitForTat()
        tournament.add_strategy(alwaysCooperate)
        tournament.add_strategy(titForTat)
        tournament.play_basic_tournament()
        assert tournament.strategy_scores[titForTat.name()] == 1200
        assert tournament.strategy_scores[alwaysCooperate.name()] == 1200
        assert (titForTat.name(), titForTat.name()) in tournament.tournament_history


    def test_play_basic_tournament_error(self):
        tournament = Tournament()
        with pytest.raises(TournamentSizeError) as excinfo:
            tournament.play_basic_tournament()
        assert str(excinfo.value) == "Tournament has to have at least 2 strategies!"


    def test_set_iterations(self):
        t = Tournament()
        assert t.iterations == 200
        t.set_iterations(100000000)
        assert t.iterations == 100000000


    def test_add_strategy_moves(self):
        t = Tournament()
        alwaysCooperate = AlwaysCooperate()
        alwaysDefect = AlwaysDefect()
        t.add_strategy(alwaysCooperate)
        t.add_strategy(alwaysDefect)
        t.set_iterations(5)
        t.play_basic_tournament()
        matchups = t.strategy_move_history
        assert matchups[alwaysCooperate.name()][alwaysDefect.name()] == [0,0,0,0,0]
        assert matchups[alwaysDefect.name()][alwaysCooperate.name()] == [1,1,1,1,1]
