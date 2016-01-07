__author__ = 'mark'
import unittest
from table import Table
from player import Player
from ai import AI
from seat import Seat
from deck import Card


class test_ai(unittest.TestCase):
    def setUp(self):
        self.player = Player('a_player', 100)
        self.seats = [Seat("a_seat")]
        self.table = Table(self.seats, 5, 10, 0)
        self.c1 = Card("c1", 2, "h")
        self.c2 = Card("c2", 2, "d")
        self.c3 = Card("c3", 3, "h")
        self.c4 = Card("c4", 7, "h")
        self.c5 = Card("c5", 7, "h")
        self.c6 = Card("c6", 7, "h")
        self.c7 = Card("c7", 7, "h")
        self.player.hole = [self.c1, self.c2]
        self.table.community_cards = [self.c3, self.c4, self.c5, self.c6, self.c7]
        self.ai = AI(self.table, self.player)

    def test_matching_values(self):
        """Can we return a dictionary with a count of each value in the hand"""

        seen = self.ai._matching_values()
        self.assertTrue(seen[3] == 1)
        self.assertTrue(seen[2] == 2)
        self.assertTrue(seen[7] == 4)

    def test_isQuads(self):
        """Can we set the quads list properly ( setup here has a quad in it)"""
        seen = self.ai._matching_values()
        self.ai._isQuads(seen)
        self.assertTrue(self.ai.quads[0] == 7)

    def test_isQuads_shared(self):
        """Can we tell if the quads are community or in the hand, if community append the Kicker to the quads list"""
        seen = self.ai._matching_values()
        self.ai._isQuads(seen)
        self.assertTrue(self.ai.quads[1] == 3)

    def test_isQuads_kicker_shared(self):
        """Can we tell if the Kicker on board quads is shared"""
        seen = self.ai._matching_values()
        self.ai._isQuads(seen)
        self.assertTrue(self.ai.quads[2] == False)

    def test_isQuads_kicker_not_shared(self):
        """ Can we tell if the kicker on board quads is not shared
        """
        self.c1.value = 12
        seen = self.ai._matching_values()
        self.ai._isQuads(seen)
        self.assertTrue(self.ai.quads[2] == True)

if __name__ == '__main__':
    unittest.main()
