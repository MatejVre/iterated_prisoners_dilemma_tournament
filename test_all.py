import pytest
import random
from src.Strategies import *

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
