"""
Holds all strategies, defined as classes. The choose_move method has to have the opponentPastMove
parameter in order to not break everything. The parameter itself is unnecessary in some cases, however.
Will see if i can add functions that retain state over multiple calls.
"""
import random

#Tested
class Strategy():

    def __init__(self, **kwargs):
        self.suffix = ""
        if "chance_of_inverse" in kwargs.keys():
            self.__chance_of_inverse = kwargs["chance_of_inverse"]
        else:
            self.__chance_of_inverse = 0
        self.__given_name = ""
        
    def name(self):
        #if a strategy does not have a given name, it means that the combination (strategy, COI) doesn't yet exist in the tournament
        if self.__given_name == "":
            if self.__chance_of_inverse == 0:
                return self.__class__.__name__
            else:
                return self.__class__.__name__ + f"-{self.__chance_of_inverse}%"
        else:
            return self.__given_name
    

    def invert_choice(self, choice):
        if choice == 0:
            return 1
        return 0
    

    def process_choice(self, choice):
        random_number = random.randint(0,99)
        if random_number < self.__chance_of_inverse:
            return self.invert_choice(choice)
        return choice
    

    def reset(self):
        pass

    def set_COI(self, COI):
        self.__chance_of_inverse = COI

    def set_given_name(self, name):
        self.__given_name = name

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

    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
        self.own_past_move = None

    def choose_move(self, opponentPastMove):
        if self.own_past_move == None:
            choice = 0
        elif opponentPastMove[-1] == self.own_past_move:
            choice = 0
        else:
            number = random.randint(0,9999)
            if number < 2857:
                choice = 0
            else:
                choice = 1
        self.own_past_move = choice
        return self.process_choice(choice)
    

    def reset(self):
        self.own_past_move = None


#Not tested completely
class Shubik(Strategy):

    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
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


class GrimTrigger(Strategy):

    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
        self.opponent_defected = False

    def choose_move(self, opponentPastMove):
        if not self.opponent_defected:
            if opponentPastMove == [] or opponentPastMove[-1] == 0:
                return self.process_choice(0)
            else:
                self.opponent_defected = True
                return self.process_choice(1)
        else:
            return self.process_choice(1)


    def reset(self):
        self.opponent_defected = False


#This rule cooperates on the first ten moves, and then if there is a defection it defects until the end of the game.
class Davis(Strategy):

    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
        self.counter = 0
        self.opponent_defected = False

    
    def choose_move(self, opponentPastMove):
        #if opponent didn't defect yet
        if not self.opponent_defected and len(opponentPastMove) != 0:
            #check last move
            self.opponent_defected = True if opponentPastMove[-1] == 1 else False

        if self.counter < 10:
            self.counter += 1
            return self.process_choice(0)
        else:        
            if self.opponent_defected:
                return self.process_choice(1)
            else:
                return self.process_choice(0)
    
    def reset(self):
        self.counter = 0
        self.opponent_defected = False

#tested   
class Joss(Strategy):

    def choose_move(self, opponentPastMove):
        if len(opponentPastMove) == 0:
            return self.process_choice(0)
        else:
            if opponentPastMove[-1] == 1:
                return self.process_choice(1)
            else:
                #simulate 90% chance of cooperation
                number = random.randint(1,10)
                if number <= 9:
                    return self.process_choice(0)
                else:
                    return self.process_choice(1)