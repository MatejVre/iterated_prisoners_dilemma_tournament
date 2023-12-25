"""
Holds all strategies, defined as classes. The choose_move method has to have the opponentPastMove
parameter in order to not break everything. The parameter itself is unnecessary in some cases, however.
Will see if i can add functions that retain state over multiple calls.
"""
import random

#Tested
class Strategy():

    def __init__(self, **kwargs):
        if len(kwargs) != 0:
            self.chance_of_inverse = kwargs["chance_of_inverse"]
        else:
            self.chance_of_inverse = 0
        
    def name(self):
        return self.__class__.__name__
    

    def invert_choice(self, choice):
        if choice == 0:
            return 1
        return 0
    

    def process_choice(self, choice):
        random_number = random.randint(0,99)
        if random_number < self.chance_of_inverse:
            return self.invert_choice(choice)
        return choice
    

    def reset(self):
        pass

#Tested
class AlwaysDefect(Strategy):

    def choose_move(self, opponentPastMove):
        return self.process_choice(1)
    
#Tested
class AlwaysCooperate(Strategy):

    def choose_move(self, opponentPastMove):
        return self.process_choice(0)
    
#Tested
class TitForTat(Strategy):

    def choose_move(self, opponentPastMove):
        if len(opponentPastMove) == 0:
            return self.process_choice(0)
        else:
            return self.process_choice(opponentPastMove[-1])
        
#Cannot test     
class RandomChoice(Strategy):

    def choose_move(self, opponentPastMove):
        return random.randint(0,1)

   
#If the players did different things on the previous move,
#this rule cooperates with probability 2/7. Otherwise this rule always cooperates
#Tested
class Grofman(Strategy):

    def __init__(self):
        Strategy.__init__(self)
        self.own_past_move = None

    def choose_move(self, opponentPastMove):
        if self.own_past_move == None:
            choice = self.process_choice(0)
        elif opponentPastMove[-1] == self.own_past_move:
            choice = self.process_choice(0)
        else:
            number = random.randint(0,9999)
            if number < 2857:
                choice = self.process_choice(0)
            else:
                choice = self.process_choice(1)
        self.own_past_move = choice
        return choice
    

    def reset(self):
        self.own_past_move = None


#Not tested completely
class Shubik(Strategy):

    def __init__(self):
        Strategy.__init__(self)
        self.num_of_opp_defects = 0
        self.upcoming_defects = 0

    def choose_move(self, opponentPastMove):
        if len(opponentPastMove) == 0:
            return self.process_choice(0)
        
        if opponentPastMove[-1] == 1:
            self.num_of_opp_defects += 1
            self.upcoming_defects += self.num_of_opp_defects
        
        if self.upcoming_defects != 0:
            self.upcoming_defects -= 1
            return self.process_choice(1)
        
        return self.process_choice(0)

    
    def reset(self):
        self.num_of_opp_defects = 0
        self.upcoming_defects = 0

