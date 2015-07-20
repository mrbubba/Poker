__author__ = 'mark'
import unittest
from player import Player
from table import Table
from dealer import Dealer
from seat import Seat
from analyzer import Analyzer
from pot import Pot


class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.p0 = Player('p0', 100)
        self.p1 = Player('p1', 100)
        self.p2 = Player('p2', 100)
        self.p3 = Player('p3', 100)
        self.p4 = Player('p4', 100)
        self.p5 = Player('p5', 100)

        self.s0 = Seat('s0')
        self.s1 = Seat('s1')
        self.s2 = Seat('s2')
        self.s3 = Seat('s3')
        self.s4 = Seat('s4')
        self.s5 = Seat('s5')

        players = [self.p0, self.p1, self.p2, self.p3, self.p4, self.p5]
        seats = [self.s0, self.s1, self.s2, self.s3, self.s4, self.s5]

        self.table = Table(seats, 5, 10, 0)
        self.dealer = Dealer(self.table)
        self.table.dealer = self.dealer

        player = 0
        for seat in seats:
            seat.player = players[player]
            seat.player.seat = seat
            seat.active = True
            seat.player.table = self.table
            player += 1

        self.table.init_hand()
        self.dealer.deal()
        self.dealer.deal()
        self.dealer.deal()
        self.analyzer = Analyzer(self.table)

    def test_flush(self):
        """Can we find a flush in the players' hands"""
        players = self.analyzer._setup()
        players = self.analyzer._order(players)
        ## a flush
        self.p0.hole[0].suit = "d"
        self.p0.hole[1].suit = "d"
        self.p0.hole[2].suit = "d"
        self.p0.hole[3].suit = "d"
        self.p0.hole[4].suit = "d"

        self.analyzer._flush(players)
        self.assertTrue(self.p0.hand)

    def test_order(self):
        """Can we order the hands in a proper order, left to right"""
        players = self.analyzer._setup()

        players = self.analyzer._order(players)
        for player in players:
            for i in range(6):
                v1 = player.hole[i].value
                v2 = player.hole[i + 1].value
                self.assertTrue(v2 <= v1)




    def test_seven_cards(self):
        """Can we get a list of players in the hand with 7 cards in the hand"""
        players = self.analyzer._setup()
        for player in players:
            self.assertTrue(len(player.hole) == 7)




if __name__ == '__main__':
    unittest.main()
