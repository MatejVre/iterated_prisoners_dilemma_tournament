"""
Holds all strategies, defined as classes. The choose_move method has to have the opponents_past_moves
parameter in order to work with the game class. The parameter itself is unnecessary in some cases, however.
"""
import random


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


class AlwaysDefect(Strategy):

    def choose_move(self, opponents_past_moves):
        return self.process_choice(1)
    

class AlwaysCooperate(Strategy):

    def choose_move(self, opponents_past_moves):
        return self.process_choice(0)
    

class TitForTat(Strategy):

    def choose_move(self, opponents_past_moves):
        if len(opponents_past_moves) == 0:
            return self.process_choice(0)
        else:
            return self.process_choice(opponents_past_moves[-1])
        
    
class RandomChoice(Strategy):

    def choose_move(self, opponents_past_moves):
        return random.randint(0,1)

   

class Grofman(Strategy):

    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
        self.own_past_move = None

    def choose_move(self, opponents_past_moves):
        if self.own_past_move == None:
            choice = 0
        elif opponents_past_moves[-1] == self.own_past_move:
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



class Shubik(Strategy):

    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
        self.num_of_opp_defects = 0
        self.upcoming_defects = 0

    def choose_move(self, opponents_past_moves):
        if len(opponents_past_moves) == 0:
            return self.process_choice(0)
        
        if opponents_past_moves[-1] == 1:
            self.num_of_opp_defects += 1
            self.upcoming_defects = self.num_of_opp_defects
        
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

    def choose_move(self, opponents_past_moves):
        if not self.opponent_defected:
            if opponents_past_moves == [] or opponents_past_moves[-1] == 0:
                return self.process_choice(0)
            else:
                self.opponent_defected = True
                return self.process_choice(1)
        else:
            return self.process_choice(1)


    def reset(self):
        self.opponent_defected = False



class Davis(Strategy):

    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
        self.counter = 0
        self.opponent_defected = False

    
    def choose_move(self, opponents_past_moves):
        #if opponent didn't defect yet
        if not self.opponent_defected and len(opponents_past_moves) != 0 and len(opponents_past_moves) < 10:
            #check last move
            self.opponent_defected = True if opponents_past_moves[-1] == 1 else False

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


class Joss(Strategy):

    def choose_move(self, opponents_past_moves):
        if len(opponents_past_moves) == 0:
            return self.process_choice(0)
        else:
            if opponents_past_moves[-1] == 1:
                return self.process_choice(1)
            else:
                #simulate 90% chance of cooperation
                number = random.randint(1,10)
                if number <= 9:
                    return self.process_choice(0)
                else:
                    return self.process_choice(1)
                


class Tullock(Strategy):
    
    def choose_move(self, opponents_past_moves):
        #first 11 moves
        if len(opponents_past_moves) < 11:
            return self.process_choice(0)
        else:
            last_ten_moves = opponents_past_moves[-10:]
            #number of 0's will be the amount of cooperations
            opponents_cooperations = last_ten_moves.count(0)
            my_cooperation_chance = opponents_cooperations - 1 #to lower it by 10 %
            #get a random integer between 1 and 10 including
            random_number = random.randint(1,10)
            #for example if opponent cooperated 4 out of 10 times, that's 40%. Minus 10% = 30%. So out of numbers 1 - 10, if
            #i pick 3 or less, i cooperate; otherwise, defect
            if random_number in range(1, (my_cooperation_chance + 1)):

                return self.process_choice(0)
            else:
                return self.process_choice(1)
            

class Anklebreaker(Strategy):
    
    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
        self.counter = 0

    def choose_move(self, opponents_past_moves):
        if opponents_past_moves == [] or self.counter != 9:
            self.counter += 1
            return self.process_choice(0)
        else:
            self.counter = 0
            return self.process_choice(1)
        
    def reset(self):
        self.counter = 0


class Adapter(Strategy):
    def __init__(self, **kwargs):
        Strategy.__init__(self, **kwargs)
        self.cooperation_chance = 70
    
    def choose_move(self, opponents_past_moves):
        if len(opponents_past_moves) == 0:
            return self.process_choice(0)
        elif len(opponents_past_moves) % 10 == 0:
            opponents_defects = sum(opponents_past_moves[-10:])
            opponents_cooperations = 10 - opponents_defects
            self.cooperation_chance += (opponents_defects - opponents_cooperations) * 2
            if self.cooperation_chance > 100:
                self.cooperation_chance == 100
            elif self.cooperation_chance < 0:
                self.cooperation_chance == 0
        random_number = random.randint(1,100)
        if self.cooperation_chance in range(1, random_number + 1):
            return self.process_choice(0)
        else:
            return self.process_choice(1)

    def reset(self):
        self.cooperation_chance = 70
    

class TitForTwoTats(Strategy):

    def choose_move(self, opponents_past_moves):
        if len(opponents_past_moves) < 2:
            return self.process_choice(0)
        elif opponents_past_moves[-2:] == [1, 1]:
            return self.process_choice(1)
        else:
            return self.process_choice(0)

