import pytest
import randtest
import random
from src.Strategies import *
from src.Game import Game
from src.Tournament import Tournament
from src.Controller import *
from src.Errors import TournamentSizeError

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
        moves_after_difference = []
        for i in range(10000):
            game.play_round()
        assert moves["strategy1"][0] == 0
        for m in range(1, (len(moves["strategy1"])-1)):
            if moves["strategy1"][m] == moves["strategy2"][m]:
                assert moves["strategy1"][m+1] == 0
            else:
                moves_after_difference.append(moves["strategy1"][m+1])
        no_moves = len(moves_after_difference)
        no_defections = sum(moves_after_difference)
        assert no_defections >= (no_moves * (5/7) - no_moves*0.1) and no_defections <= (no_moves * (5/7) + no_moves*0.1)


    def test_Shubik(self):
        shubik = Shubik()
        alwaysCooperate = AlwaysCooperate()
        game = Game()
        game.strategy1 = shubik
        game.strategy2 = alwaysCooperate
        moves = game.player_moves
        for i in range(10):
            game.play_round()
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
            game.play_round()
        for move in moves["strategy1"]:
            assert move == 0
        grimTrigger.reset()
        game2 = Game()
        random = RandomChoice()
        game2.strategy1 = grimTrigger
        game2.strategy2 = random
        #test that if a defection occurs, all other choices are defect
        for i in range(30):
            game2.play_round()
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
            game.play_round()
        for move in moves["strategy1"]:
            assert move == 0
        game.clear()
        game.strategy2 = random
        for i in range(30):
            game.play_round()
        for move in moves["strategy1"][10:]:
            assert move == 1

    
    def test_Joss(self):
        joss = Joss()
        random = RandomChoice()
        alwaysCooperate = AlwaysCooperate()
        game = Game()
        moves = game.player_moves
        game.strategy1 = joss
        game.strategy2 = random
        #check defection after each defection
        for i in range(100):
            game.play_round()
        for i in range(99):
            if moves["strategy2"][i] == 1:
                assert moves["strategy1"][i+1] == 1
        game.clear()
        game.strategy2 = alwaysCooperate
        for i in range(1000):
            game.play_round()
        #should be around 90% of cooperations
        assert sum(moves["strategy1"]) >= 90 and sum(moves["strategy1"]) <= 110
        
                
    def test_RandomChoice(self):
        random = RandomChoice()
        joss = Joss()
        game = Game()
        moves = game.player_moves
        game.strategy1 = joss
        game.strategy2 = random
        for i in range(1000):
            game.play_round()
        assert randtest.random_score(moves["strategy2"])


    def test_process_choice(self):
        alwaysCooperate = AlwaysCooperate(chance_of_inverse=5)
        alwaysDefect = AlwaysDefect(chance_of_inverse=5)
        game = Game()
        moves = game.player_moves
        game.strategy1 = alwaysCooperate
        game.strategy2 = alwaysDefect
        for i in range(1000):
            game.play_round()
        assert randtest.random_score(moves["strategy1"]) and randtest.random_score(moves["strategy2"])
        

    def test_Tullock(self):
        tullock = Tullock()
        alwaysDefect = AlwaysDefect()
        game = Game()
        game.strategy1 = tullock
        game.strategy2 = alwaysDefect
        moves = game.player_moves
        for i in range(20):
            game.play_round()
        print(moves)
        #test first 11 are cooperations
        for x in range(11):
            assert moves["strategy1"][x] == 0
        #all after move 11 should be defections
        for n in range(14,20):
            assert moves["strategy1"][n] == 1


    def test_Anklebreaker(self):
        random = RandomChoice()
        anklebreaker = Anklebreaker()
        game = Game()
        game.strategy1 = anklebreaker
        game.strategy2 = random
        moves = game.player_moves
        for i in range(100):
            game.play_round()
        print(moves["strategy1"])
        assert moves["strategy1"][0] == 0
        assert moves["strategy1"][9] == 1
        
        supposed_defects = moves["strategy1"][9:-1:10]
        for x in supposed_defects:
            assert x == 1

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

    
    def test_set_iterations(self):
        t = Tournament()
        assert t.iterations == 200
        t.set_iterations(100000000)
        assert t.iterations == 100000000


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
        list = [s.name() for s in c.tournament.list_of_strategies]
        assert  "TitForTat" in list
        assert "TitForTat-1" in list

    def test_remove_strategy_from_tournament(self):
        c = Controller()
        c.fill_with_basic_strategies()
        assert c.remove_strategy_from_tournament("TitForTat") == True
        assert c.remove_strategy_from_tournament("Random name that deffinitely does not work") == False

    