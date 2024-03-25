import pytest
import randtest
import random
from src.Model.Strategies import *
from src.Model.Game import Game


class Test_Strategies():


    def test_AlwaysDefect(self):
        #basic cases
        assert AlwaysDefect().choose_move(1) == 1
        assert AlwaysDefect().choose_move(0) == 1


    def test_AlwaysCooperate(self):
        #basic cases
        assert AlwaysCooperate().choose_move(0) == 0
        assert AlwaysCooperate().choose_move(1) == 0


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


    def test_Grofman(self):
        grofman = Grofman()
        random = RandomChoice()
        game = Game(grofman, random)
        moves = game.player_moves
        moves_after_difference = []
        for i in range(10000):
            game.play_round()
        assert moves[grofman][0] == 0
        for m in range(1, (len(moves[grofman])-1)):
            if moves[grofman][m] == moves[random][m]:
                assert moves[grofman][m+1] == 0
            else:
                moves_after_difference.append(moves[grofman][m+1])
        no_moves = len(moves_after_difference)
        no_defections = sum(moves_after_difference)
        assert (no_defections >= (no_moves * (5/7) - no_moves*0.1) 
                and no_defections <= (no_moves * (5/7) + no_moves*0.1))

    #test??????
    def test_Shubik(self):
        shubik = Shubik()
        alwaysCooperate = AlwaysCooperate()
        game = Game(shubik, alwaysCooperate)
        moves = game.player_moves
        for i in range(10):
            game.play_round()
        for move in moves[shubik]:
            assert move == 0

    def test_GrimTrigger(self):
        grimTrigger = GrimTrigger()
        alwaysCooperate = AlwaysCooperate()
        random = RandomChoice()
        game = Game(grimTrigger, alwaysCooperate)
        moves = game.player_moves
        #Tests that starts with 0
        for i in range(10):
            game.play_round()
        for move in moves[grimTrigger]:
            assert move == 0
        grimTrigger.reset()
        game2 = Game(grimTrigger, random)
        #test that if a defection occurs, all other choices are defect
        for i in range(30):
            game2.play_round()
        for m in game2.player_moves[grimTrigger][game2.player_moves[random].index(1) +1 :]:
            assert m == 1

    #is random really the best choice?
    def test_Davis(self):
        davis = Davis()
        alwaysCooperate = AlwaysCooperate()
        random = RandomChoice()
        game = Game(davis, alwaysCooperate)
        moves = game.player_moves
        #Tests that starts with 0
        for i in range(100):
            game.play_round()
        for move in moves[davis]:
            assert move == 0
        game = Game(davis, random)
        moves = game.player_moves
        for i in range(30):
            game.play_round()
        for move in moves[davis][10:]:
            assert move == 1

    
    def test_Joss(self):
        joss = Joss()
        random = RandomChoice()
        alwaysCooperate = AlwaysCooperate()
        game = Game(joss, random)
        moves = game.player_moves
        #check defection after each defection
        for i in range(100):
            game.play_round()
        for i in range(99):
            if moves[random][i] == 1:
                assert moves[joss][i+1] == 1
        game = Game(joss, alwaysCooperate)
        moves = game.player_moves
        for i in range(10000):
            game.play_round()
        #should be around 90% of cooperations
        assert sum(moves[joss]) >= 900 and sum(moves[alwaysCooperate]) <= 1100
        
                
    def test_RandomChoice(self):
        random = RandomChoice()
        joss = Joss()
        game = Game(random, joss)
        moves = game.player_moves
        for i in range(1000):
            game.play_round()
        assert randtest.random_score(moves[random])


    def test_process_choice(self):
        alwaysCooperate = AlwaysCooperate(chance_of_inverse=10)
        alwaysDefect = AlwaysDefect(chance_of_inverse=10)
        game = Game(alwaysCooperate, alwaysDefect)
        moves = game.player_moves
        for i in range(10000):
            game.play_round()
        ac_moves = moves[alwaysCooperate]
        ac_cooperations = ac_moves.count(0)
        assert ac_cooperations >= 8100 and ac_cooperations <= 9900
        

    def test_Tullock(self):
        tullock = Tullock()
        alwaysDefect = AlwaysDefect()
        alwaysCooperate = AlwaysCooperate()
        game = Game(tullock, alwaysDefect)
        moves = game.player_moves
        for i in range(20):
            game.play_round()
        #test first 11 are cooperations
        for x in range(11):
            assert moves[tullock][x] == 0
        #all after move 11 should be defections
        for n in range(14,20):
            assert moves[tullock][n] == 1
        game = Game(tullock, alwaysCooperate)
        moves = game.player_moves
        for i in range(10000):
            game.play_round()
        count = moves[tullock][11:].count(0)
        assert count > 8100 and count < 9900


    def test_Anklebreaker(self):
        random = RandomChoice()
        anklebreaker = Anklebreaker()
        game = Game(anklebreaker, random)
        moves = game.player_moves
        for i in range(100):
            game.play_round()
        print(moves[anklebreaker])
        assert moves[anklebreaker][0] == 0
        assert moves[anklebreaker][9] == 1
        supposed_defects = moves[anklebreaker][9:-1:10]
        for x in supposed_defects:
            assert x == 1  
    

    def test_TitForTwoTats(self):
        random = RandomChoice()
        tftt = TitForTwoTats()
        game = Game(random, tftt)
        for _ in range(200):
            game.play_round()
        moves = game.player_moves
        assert moves[tftt][0] == 0
        assert moves[tftt][1] == 0
        for i in range(198):
            if moves[random][i] == 1 and moves[random][i + 1] == 1:
                assert moves[tftt][i + 2] == 1
        