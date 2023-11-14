"""
Holds all strategies, defined as classes. The chooseMove method has to have the opponentPastMove
parameter in order to not break everything. The parameter itself is unnecessary in some cases, however.
Will see if i can add functions that retain state over multiple calls.
"""
import random

class AlwaysDefect:

    def chooseMove(self, opponentPastMove):
        return 1
    

class AlwaysCooperate:

    def chooseMove(self, opponentPastMove):
        return 0
    
class TitForTat:

    def chooseMove(self, opponentPastMove):
        if len(opponentPastMove) == 0:
            return 0
        else:
            return opponentPastMove[-1]
        
class RandomChoice:

    def chooseMove(self, opponentPastMove):
        return random.randint(0,1)
    

