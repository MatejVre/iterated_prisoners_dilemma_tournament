"""
This is the game class which is used to run the game.
Result matrix based off of:
                Player 1
                Cooperate   Defect
 -----------+----------------------
 Player 2   |
 Cooperate  |    (2,2)      (5,0)
            |
 Defect     |    (0,5)      (1,1)
 -----------------------------------
 The numbers for the lengths of statements are symbollic
 and will most likely change during the coding process

 Since the user input is binary, 0 and 1 will be used for 
 Cooperate and Defect respectively. 
"""

class Game:



    def __init__(self):
        #self.strategy1 = strategy1
        #self.strategy2 = strategy2
        self.player_moves = dict(strategy1 = [], strategy2 = [])
        self.ZERO = 0
        self.MINIMUM_PAYOFF = 1
        self.MEDIUM_PAYOFF = 3
        self.MAXIMUM_PAYOFF = 5
        self.RESULT_MATRIX = [[(self.MEDIUM_PAYOFF, self.MEDIUM_PAYOFF), (self.MAXIMUM_PAYOFF, self.ZERO)],
                     [(self.ZERO, self.MAXIMUM_PAYOFF), (self.MINIMUM_PAYOFF, self.MINIMUM_PAYOFF)]]
        self.game_history = []
        self.strategy1 = None
        self.strategy2 = None

    
    def play_round(self):
        strategy1_move = self.strategy1.choose_move(self.player_moves["strategy2"])
        strategy2_move = self.strategy2.choose_move(self.player_moves["strategy1"])

        result = self.RESULT_MATRIX[strategy2_move][strategy1_move]

        self.player_moves["strategy1"].append(strategy1_move)
        self.player_moves["strategy2"].append(strategy2_move)
        self.game_history.append(result)
        #print(result)
    
    #gets total served time of both of the strategy
    #returns [time_for_strategy1, time_for_strategy2]
    def add_payoffs(self):
        result = [0,0]
        for outcome in self.game_history:
            result[0] += outcome[0]
            result[1] += outcome[1]
        return result
    
    #clears the game history
    def clear_game_history(self):
        self.game_history = []

    #clears both players histories
    def clear_player_moves(self):
        self.player_moves["strategy1"] = []
        self.player_moves["strategy2"] = []
    
    def clear(self):
        self.clear_game_history()
        self.clear_player_moves()

"""
game = Game()
game.playGame(0,0)
game.playGame(0,1)
game.playGame(1,0)
game.playGame(1,1)
"""