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
    

