__author__ = 'mark'
from seat import Seat
from table import Table
from pot import Pot
from player import Player

class Analyzer(object):
    """ Analyzer object

    Attributes:

       table(obj):  table object
       poker_hands(dic): refers poker hands to numbers eg Pair will = 1

    We will represent the poker hands thusly:
        straight flush: [8, 14] for highest possible and [8,5] for lowest possible flush
        4 of Kind: ( four tens w/ ace kicker ) : [ 7,10,14]
        full house: ( queens full of nines ) : [ 6,12,9]
        flush : ( flush withking, jack, nine, six and a four ) : [ 5, 13,11,9,6,4 ]
        straight: ( nine, eight, seven, six, five ): [ 4,9,8,7,6,5]
        three of a kind: ( 6 kinds and a Ace and a King ) : [ 3,6,14,13]
        two pair: ( eights and fours and an ace ) : [ 2,8,4,14]
        pair: ( two nine, and ace, 10 and a 7 )  : [ 1,14,10,7]
        high card : ( jack, ten, nine, eight, five ) : [ 0,11,10,9,8,5]

    Methods:

        analyze:    gets the community cards and list of pots from the dealer,
                    for each pot awards the chips to the winner/s
                    If an all in player wins, analyze will reset that seats
                    active to True
    """

    def __init__(self, table):
        self.table = table
        # self.pot = self.table.pots.pop()
        self.pot = self.table.pots[0]
        self.poker_hands = {"HighCard": 0,
                            "Pair": 1,
                            "TwoPair": 2,
                            "ThreeOfAKind": 3,
                            "Straight": 4,
                            "Flush": 5,
                            "FullHouse": 6,
                            "FourOfAKind": 7,
                            "StraightFlush": 8}

    def _flush(self, players):
        """Identify those hands that are flushes"""
        for player in players:
            suits ={'d': [], 'h': [], 's': [], 'c': []}
            for card in player.hole:
                x = card.suit
                suits[x].append(card)
            for suit in suits:
                if len(suits[suit]) >= 5:
                    player.hand.append('Flush')
                    player.hand += suits[suit]

        return players

    def _order(self, players):
        """order players' hands from highest to lowest"""
        for player in players:
            player.hole.sort(key=lambda x: x.value, reverse=True)
        return players

    def _setup(self):
        """get the players in the pot and their hands"""
        players = []

        """ yes this appending is correct """

        for seat in self.pot.seats:
            if seat.active:
                players.append(seat.player)

        """ yes this appending is correct ( because players have been removed from pot.seats if all_in"""
        for seat in self.pot.all_in:
            players.append(seat.player)

        for player in players:
            player.hole += self.table.community_cards

        return players

