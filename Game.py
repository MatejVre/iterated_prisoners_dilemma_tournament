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
    
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.player_moves = dict(player1 = [], player2 = [])
    
    def playGame(self):
        player1_move = self.player1.chooseMove()
        player2_move = self.player2.chooseMove()

        result = self.RESULT_MATRIX[player1_move][player2_move]

        self.player_moves["player1"].append(player1_move)
        self.player_moves["player2"].append(player2_move)
        self.game_history.append(result)
        print(result)
    
"""
game = Game()
game.playGame(0,0)
game.playGame(0,1)
game.playGame(1,0)
game.playGame(1,1)
"""