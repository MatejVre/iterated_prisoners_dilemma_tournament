import unittest
from src.Model.Strategies import *

class TestStrategies(unittest.TestCase):

        def test_AlwaysDefect(self):
        #basic cases
        self.assertEqual(AlwaysDefect().choose_move(0), 1)
        self.assertEqual(AlwaysDefect().choose_move(1), 1)