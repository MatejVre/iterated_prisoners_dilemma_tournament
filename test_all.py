import pytest
import random
from src.Strategies import *
from src.Game import Game
#from src.Tournament import Tournament

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

    
    def test_invert_choice(self):
        assert Strategy().invert_choice(0) == 1
        assert Strategy().invert_choice(1) == 0


    #Cannot test the entire strategy since one
    #of the conditions work with a random
    def test_Grofman(self):
        grofman = Grofman()
        random = RandomChoice()
        game = Game()
        game.strategy1 = grofman
        game.strategy2 = random
        moves = game.player_moves
        for i in range(10):
            game.playGame()
        assert moves["strategy1"][0] == 0
        for m in range(1, (len(moves["strategy1"])-1)):
            if moves["strategy1"][m] == moves["strategy2"][m]:
                assert moves["strategy1"][m+1] == 0


    def test_Shubik(self):
        shubik = Shubik()
        alwaysCooperate = AlwaysCooperate()
        game = Game()
        game.strategy1 = shubik
        game.strategy2 = alwaysCooperate
        moves = game.player_moves
        for i in range(10):
            game.playGame()
        for move in moves["strategy1"]:
            assert move == 0


class TestGameFunctions():

    game = Game()
    game.strategy1 = TitForTat()
    game.strategy2 = TitForTat()
    
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


class TestTournamentFunctions():


    def get_unique_strategy_pairs():
        pass
