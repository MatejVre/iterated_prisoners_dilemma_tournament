class Player:

    def __init__(self, strategy):
        self.strategy = strategy

    def chooseMove(self):
        return self.strategy()