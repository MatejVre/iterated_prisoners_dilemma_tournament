import pytest
from src.Model.Game import Game
from src.Model.Strategies import *

class Test_Game:

    game = Game(TitForTat(), TitForTat())

    def test_play_round(self):
        g = self.game
        g.play_round()
        assert g.game_history[0] == (3,3)
        for key in g.player_moves:
            assert g.player_moves[key] == [0]

    def test_add_payoffs(self):
        g = Game(TitForTat(), TitForTat())
        for _ in range(200):
            g.play_round()
        result = g.add_payoffs()
        assert result == [600, 600]        

    def test_clear_history(self):
        g = self.game
        g.game_history = [[3,1],[1,3],[2,2]]
        g.clear_game_history()
        assert g.game_history == []

    def test_clear_player_moves(self):
        g = self.game
        g.play_round()
        g.clear_player_moves()
        for key in g.player_moves:
            assert g.player_moves[key] == []