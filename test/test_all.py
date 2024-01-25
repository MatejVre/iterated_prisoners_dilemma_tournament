import pytest
import random
from src.Strategies import *
from src.Game import Game
from src.Tournament import Tournament
from src.Controller import Controller

class TestStrategies():

    COOPERATE = 0
    DEFECT = 1

    def test_AlwaysDefect(self):
        #basic cases
        assert AlwaysDefect().choose_move(self.COOPERATE) == 1
        assert AlwaysDefect().choose_move(self.DEFECT) == 1


    def test_AlwaysCooperate(self):
        #basic cases
        assert AlwaysCooperate().choose_move(self.COOPERATE) == 0
        assert AlwaysCooperate().choose_move(self.DEFECT) == 0


    def test_TitForTat(self):
        #basic cases
        assert TitForTat().choose_move([]) == 0
        assert TitForTat().choose_move([1]) == 1
        assert TitForTat().choose_move([0]) == 0
        #other cases
        history = [0,0,0,0,0,1,1,1,1,1]
        random.shuffle(history)
        assert TitForTat().choose_move(history) == history[-1]

    
    def test_invert_choice(self):
        assert Strategy().invert_choice(0) == 1
        assert Strategy().invert_choice(1) == 0


    #Cannot test the entire strategy since one
    #of the conditions work with a random
    #ASK JULES 
    def test_Grofman(self):
        grofman = Grofman()
        random = RandomChoice()
        game = Game()
        game.strategy1 = grofman
        game.strategy2 = random
        moves = game.player_moves
        for i in range(10):
            game.play_game()
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
            game.play_game()
        for move in moves["strategy1"]:
            assert move == 0

    def test_GrimTrigger(self):
        grimTrigger = GrimTrigger()
        alwaysCooperate = AlwaysCooperate()
        game = Game()
        game.strategy1 = grimTrigger
        game.strategy2 = alwaysCooperate
        moves = game.player_moves
        #Tests that starts with 0
        for i in range(10):
            game.play_game()
        for move in moves["strategy1"]:
            assert move == 0
        grimTrigger.reset()
        game2 = Game()
        random = RandomChoice()
        game2.strategy1 = grimTrigger
        game2.strategy2 = random
        #test that if a defection occurs, all other choices are defect
        for i in range(30):
            game2.play_game()
        for m in game2.player_moves["strategy1"][game2.player_moves["strategy2"].index(1) +1 :]:
            assert m == 1

    #is random really the best choice?
    def test_Davis(self):
        davis = Davis()
        alwaysCooperate = AlwaysCooperate()
        alwaysDefect = AlwaysDefect()
        random = RandomChoice()
        game = Game()
        game.strategy1 = davis
        game.strategy2 = alwaysCooperate
        moves = game.player_moves
        #Tests that starts with 0
        for i in range(100):
            game.play_game()
        for move in moves["strategy1"]:
            assert move == 0
        game.clear()
        game.strategy2 = random
        for i in range(30):
            game.play_game()
        for move in moves["strategy1"][10:]:
            assert move == 1

    
    def test_Joss(self):
        joss = Joss()
        random = RandomChoice()
        game = Game()
        moves = game.player_moves
        game.strategy1 = joss
        game.strategy2 = random
        #check defection after each defection
        for i in range(100):
            game.play_game()
        for i in range(99):
            if moves["strategy2"][i] == 1:
                assert moves["strategy1"][i+1] == 1
        #ask Jules again how to test Random behaviour
        #is this even random behaviour??




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

    def test_reset(self):
        t = Tournament([Shubik(), Grofman()])
        t.play_basic_tournament()
        t.reset()
        assert t.tournament_history == {}
        for strat in t.listOfStrategies:
            assert t.strategy_scores[strat.name()] == 0


class TestControllerFunctions():

    def test_add_strategy(self):
        c = Controller()
        s1 = c.add_strategy("TitForTat", 1)
        s2 = c.add_strategy("TitForTat", 1)
        s3 = c.add_strategy("Joss", 0)

        assert s1 != s2
        assert s1.name() == "TitForTat-1%"
        assert s3.name() == "Joss"

    def test_name_strategy(self):
        c = Controller()
        c.add_strategy("TitForTat", 0)
        c.add_strategy("TitForTat", 0)
        list = [s.name() for s in c.custom_list_of_strategies]
        assert  "TitForTat" in list
        assert "TitForTat-1" in list