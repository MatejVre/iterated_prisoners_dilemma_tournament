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
    LET_GO = 0
    MINIMUM_SENTENCE = 1
    MEDIUM_SENTENCE = 2
    MAXIMUM_SENTENCE = 3
    RESULT_MATRIX = [[(MEDIUM_SENTENCE, MEDIUM_SENTENCE), (MAXIMUM_SENTENCE, LET_GO)],
                     [(LET_GO, MAXIMUM_SENTENCE), (MINIMUM_SENTENCE, MINIMUM_SENTENCE)]]
    game_history = []
    player_moves = {}
    
    def __init__(self, strategy1, strategy2):
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.player_moves = dict(strategy1 = [], strategy2 = [])
    
    def playGame(self):
        strategy1_move = self.strategy1.chooseMove(self.player_moves["strategy2"])
        strategy2_move = self.strategy2.chooseMove(self.player_moves["strategy1"])

        result = self.RESULT_MATRIX[strategy1_move][strategy2_move]

        self.player_moves["strategy1"].append(strategy1_move)
        self.player_moves["strategy2"].append(strategy2_move)
        self.game_history.append(result)
        #print(result)
    
    def addServedTime(self):
        result = [0,0]
        for outcome in self.game_history:
            result[0] += outcome[0]
            result[1] += outcome[1]
        return result

"""
game = Game()
game.playGame(0,0)
game.playGame(0,1)
game.playGame(1,0)
game.playGame(1,1)
"""