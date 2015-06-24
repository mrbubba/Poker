import unittest
from deck import Card, Deck
from player import Player
from table import Table
from dealer import Dealer
from seat   import Seat
from pot    import Pot

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
        self.p1 = Player('p1', 100)
        self.p2 = Player('p2', 100)
        self.p3 = Player('p3', 0)
        self.p4 = Player('p4', 100)


        self.s1 = Seat('s1')
        self.s2 = Seat('s2')
        self.s3 = Seat('s3')
        self.s4 = Seat('s4')

        players = [self.p1, self.p2, self.p3, self.p4]
        seats = [self.s1, self.s2, self.s3, self.s4]

        self.table = Table(seats, 5, 10, 0)
        self.dealer = Dealer(self.table)
        self.table.dealer = self.dealer

        i = 0
        for seat in seats:
            seat.player = players[i]
            seat.active = True
            seat.player.table = self.table
            i += 1

    def test_remove_0_stack(self):
        """Does dealer remove broke players at the start of a hand??"""
        self.setUp()
        self.dealer._remove_0_stack()

        self.assertFalse(self.table.seats[2].active)

    def test_deal_hole(self):
        """can the dealer deal two cards to each player??"""
        self.table.seats[2].active = False
        self.dealer._deal_hole()
        # only want the active players
        players = []
        for seat in self.table.seats:
            if seat.active:
                players.append(seat.player)
        # active players should have cards
        for player in players:
            self.assertEqual(len(player.hole), 2)
        # inactive players shouldn't have cards
        self.assertEqual(len(self.table.seats[2].player.hole), 0)


class TestPlayer(unittest.TestCase):
    """Do we have working player objects?"""


class TestTable(unittest.TestCase):
    """Do we have a working table object?"""

    def setUp(self):
        self.p1 = Player('p1', 100)
        self.p2 = Player('p2', 100)
        self.p3 = Player('p3', 100)
        self.p4 = Player('p4', 100)


        self.s1 = Seat('s1')
        self.s2 = Seat('s2')
        self.s3 = Seat('s3')
        self.s4 = Seat('s4')

        players = [self.p1, self.p2, self.p3, self.p4]
        seats = [self.s1, self.s2, self.s3, self.s4]

        self.table = Table(seats, 5, 10, 0)
        self.dealer = Dealer(self.table)
        self.table.dealer = self.dealer

        i = 0
        for seat in seats:
            seat.player = players[i]
            seat.active = True
            seat.player.table = self.table

    def test_button_move(self):
        """Can we move the button and the blinds appropriately?"""
        s1 = Seat('s1')
        s2 = Seat('s2')
        s3 = Seat('s3')

        s1.active = True
        s2.active = True
        s3.active = True
        seats = [s1, s2, s3]
        table = Table(seats, 5, 10)
        table.big_blind = 1
        table._button_move()
        self.assertEqual(table.button, 0)
        self.assertEqual(table.small_blind, 1)
        self.assertEqual(table.big_blind, 2)

    def test_button_move_head_to_head(self):
        """Can we move the blinds and button appropriately head to head?"""
        s1 = Seat('s1')
        s2 = Seat('s2')
        s1.active = True
        s2.active = True
        seats = [s1, s2]
        table = Table(seats, 5, 10)
        table.big_blind = 0
        table._button_move()
        self.assertEqual(table.button, 0)
        self.assertEqual(table.small_blind, 0)
        self.assertEqual(table.big_blind, 1)

    def test_set_button(self):
        """can we randomly set the button for initial play on active seats only??"""
        self.table.seats[2].active = False
        self.table.set_button()
        a = self.table.button
        self.assertTrue(self.table.seats[self.table.button].active)
        self.table.set_button()
        b = self.table.button
        self.assertTrue(self.table.seats[self.table.small_blind].active)
        self.table.set_button()
        c = self.table.button
        self.assertTrue(self.table.seats[self.table.big_blind].active)
        self.table.set_button()
        d = self.table.button
        self.assertTrue(self.table.seats[self.table.under_the_gun].active)
        self.table.set_button()
        e = self.table.button
        self.assertTrue(self.table.seats[self.table.button].active)
        self.table.set_button()
        f = self.table.button
        self.assertTrue(self.table.seats[self.table.button].active)
        self.assertFalse(a == b == c == d == e == f)

        """can we set the button/blinds correctly head to head?"""

        self.table.seats[3].active = False
        self.table.set_button()
        self.assertEqual(self.table.button, self.table.small_blind)
        self.assertEqual(self.table.button, self.table.under_the_gun)
        self.assertFalse(self.table.button == self.table.big_blind)

    def test_create_pot(self):
        """ can we spawn a pot object properly? """
        pot = self.table._create_pot()



        self.assertEqual(len(self.table.pots), 1)
        self.assertEqual(pot.increment, 10)

    def test_reset(self):
        """ Can we reset for a new hand??"""





if __name__ == '__main__':
    unittest.main()
