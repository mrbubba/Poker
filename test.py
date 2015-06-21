import unittest
from deck import Card, Deck
from player import Player
from table import Table
from dealer import Dealer


class TestDeck(unittest.TestCase):
    """Do We have a working deck??"""

    def setUp(self):
        self.deck = Deck()
        self.deck.create()

    def test_create(self):
        """Can we create a deck?"""
        self.assertTrue(len(self.deck.deck) == 52)
        self.assertFalse(self.deck.deck[0].name == self.deck.deck[1].name)

    def test_deal(self):
        dealt_card = self.deck.deck[0]
        next_card = self.deck.deck[1]
        result = self.deck.deal()
        self.assertEqual(result, dealt_card)
        self.assertEqual(self.deck.deck[0], next_card)


class TestDealer(unittest.TestCase):
    """Do we have a functioning Dealer?"""

    def setUp(self):
        p1 = Player('p1', 100)
        p2 = Player('p2', 100)
        p3 = Player('p3', 0)
        p4 = Player('p4', 100)

        players = [p1, p2, p3, p4]
        self.table = Table(players, 5, 10, 0)
        self.dealer = Dealer(self.table)
        self.table.dealer = self.dealer

    def test_set_no_small_blind(self):
        """can we set table.no_small_blind to true when appropriate?"""
        self.table.big_blind = 2
        self.dealer._remove_0_stack()
        self.assertTrue(self.table.no_small_blind)

    def test_remove_0_stack(self):
        """Does dealer remove broke players at the start of a hand??"""
        self.setUp()
        self.dealer._remove_0_stack()

        self.assertEqual(len(self.table.players), 3)

    def test_deal_hole(self):
        """can the dealer deal two cards to each player??"""
        self.dealer._deal_hole()
        players = self.table.players
        for player in players:
            self.assertEqual(len(player.hole), 2)


class TestPlayer(unittest.TestCase):
    """Do we have working player objects?"""


class TestTable(unittest.TestCase):
    """Do we have a working table object?"""

    def test_button_move(self):
        """Can we move the button and the blinds appropriately?"""
        p1 = Player('p1', 100)
        p2 = Player('p2', 100)
        p3 = Player('p3', 100)
        players = [p1, p2, p3]
        table = Table(players, 5, 10)
        table.button = 2
        table._button_move()
        self.assertEqual(table.button, 0)
        self.assertEqual(table.small_blind, 1)
        self.assertEqual(table.big_blind, 2)

    def test_button_move_head_to_head(self):
        """Can we move the blinds and button appropriately head to head?"""
        p1 = Player('p1', 100)
        p2 = Player('p2', 100)
        players = [p1, p2]
        table = Table(players, 5, 10)
        table.button = 1
        table._button_move()
        self.assertEqual(table.button, 0)
        self.assertEqual(table.small_blind, 0)
        self.assertEqual(table.big_blind, 1)

    def test_flush(self):
        pass


if __name__ == '__main__':
    unittest.main()
