"""
This is the game class which is used to run the game.
Result matrix based off of:
                Player 1
                Cooperate   Defect
 -----------+----------------------
 Player 2   |
 Cooperate  |    (2,2)      (3,0)
            |
 Defect     |    (0,3)      (1,1)
 -----------------------------------
 The numbers for the lengths of statements are symbollic
 and will most likely change during the coding process

 Since the user input is binary, 0 and 1 will be used for 
 Cooperate and Defect respectively. 
"""

class Game:
    ZERO = 0
    MINIMUM_PAYOFF = 1
    MEDIUM_PAYOFF = 3
    MAXIMUM_PAYOFF = 5
    RESULT_MATRIX = [[(MEDIUM_PAYOFF, MEDIUM_PAYOFF), (MAXIMUM_PAYOFF, ZERO)],
                     [(ZERO, MAXIMUM_PAYOFF), (MINIMUM_PAYOFF, MINIMUM_PAYOFF)]]
    game_history = []
    player_moves = {}
    strategy1 = None
    strategy2 = None


    def __init__(self):
        #self.strategy1 = strategy1
        #self.strategy2 = strategy2
        self.player_moves = dict(strategy1 = [], strategy2 = [])

    
    def play_game(self):
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

"""
game = Game()
game.playGame(0,0)
game.playGame(0,1)
game.playGame(1,0)
game.playGame(1,1)
"""