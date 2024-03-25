#Errors have been defined to provide a more "elegant",
#solution. Because of said error classes, exceptions
#can be handled using try/catch clauses instead of if statements.
class TournamentSizeError(Exception):
    pass

class DataError(Exception):
    pass