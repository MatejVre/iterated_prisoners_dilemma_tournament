"""
Player class, takes a strategy function which helps
it decide what move to go for next
PROBABLY WILL NOT BE USED ANYMORE BUT WILL BE KEPT HERE JUST IN CASE FOR NOW
"""
class Player:

    def __init__(self, strategy):
        self.strategy = strategy
        self.pastMoves = []

    def chooseMove(self):
        pick = self.strategy()
        self.pastMoves.append(pick)
        return pick
    
    def getLastMove(self):
        return self.pastMoves[-1]
