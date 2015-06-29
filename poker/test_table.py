__author__ = 'mark'
import unittest
from player import Player
from table import Table
from dealer import Dealer
from seat   import Seat


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
        self.table.seats[2].active = False
        self.table.set_button()
        self.assertEqual(self.table.button, self.table.small_blind)
        self.assertEqual(self.table.button, self.table.under_the_gun)
        self.assertFalse(self.table.button == self.table.big_blind)

    def test_button_move(self):
        """Can we move the button and the blinds appropriately?"""
        s1 = Seat('s1')
        s2 = Seat('s2')
        s3 = Seat('s3')
        s4 = Seat('s4')

        s1.active = True
        s2.active = True
        s3.active = True
        s4.active = True
        seats = [s1, s2, s3, s4]
        table = Table(seats, 5, 10)
        table.small_blind = 0
        table.big_blind = 1
        table._button_move()
        self.assertEqual(table.button, 0)
        self.assertEqual(table.small_blind, 1)
        self.assertEqual(table.big_blind, 2)
        self.assertEqual(table.under_the_gun, 3)

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
        self.assertEqual(table.under_the_gun, 0)

    def test_create_pot(self):
        """ can we spawn a pot object properly? """
        pot = self.table._create_pot()

        self.assertEqual(len(self.table.pots), 1)
        self.assertEqual(pot.increment, 10)

    def test_reset_players(self):
        """ Can we reset for a new hand??"""
        self.table.seats[0].player.equity = 50
        self.table.seats[0].player.hole = [1, 2, 3]
        self.table._reset_players()
        self.assertTrue(self.table.seats[0].player.equity == 0)
        self.assertEqual(len(self.table.seats[0].player.hole), 0)

    def test_remove_0_stack(self):
        """Does the table remove broke players at the start of a hand??"""
        self.setUp()
        self.table.seats[2].player.stack = 0
        self.table._remove_0_stack()
        self.assertFalse(self.table.seats[2].active)
