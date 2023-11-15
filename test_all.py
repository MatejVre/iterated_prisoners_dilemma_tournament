import pytest
import random
from src.Strategies import *
from src.Game import Game


class TestStrategies():

    COOPERATE = 0
    DEFECT = 1

    def test_AlwaysDefect(self):
        #basic cases
        assert AlwaysDefect().chooseMove(self.COOPERATE) == 1
        assert AlwaysDefect().chooseMove(self.DEFECT) == 1


    def test_AlwaysCooperate(self):
        #basic cases
        assert AlwaysCooperate().chooseMove(self.COOPERATE) == 0
        assert AlwaysCooperate().chooseMove(self.DEFECT) == 0


    def test_TitForTat(self):
        #basic cases
        assert TitForTat().chooseMove([]) == 0
        assert TitForTat().chooseMove([1]) == 1
        assert TitForTat().chooseMove([0]) == 0
        #other cases
        history = [0,0,0,0,0,1,1,1,1,1]
        random.shuffle(history)
        assert TitForTat().chooseMove(history) == history[-1]


class TestGameFunctions():

    game = Game(TitForTat(), AlwaysDefect())
    
    def test_clear_history(self):
        g = self.game
        g.game_history = [[3,1],[1,3],[2,2]]
        g.clear_game_history()
        assert g.game_history == []


    def test_clear_player_moves(self):
        g = self.game
        g.player_moves = dict(strategy1 = [1,0,0,0,1], strategy2 = [0,1,1,1,1])
        g.clear_player_moves()
        assert g.player_moves["strategy1"] == []
        assert g.player_moves["strategy2"] == []
