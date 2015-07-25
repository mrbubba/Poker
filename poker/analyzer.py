__author__ = 'mark'
from seat import Seat
from table import Table
from pot import Pot
from player import Player

class Analyzer(object):
    """ Analyzer object

    Attributes:

       table(obj):  table object
       poker_hands(lst): refers poker hands to numbers eg Pair will = 1

    We will represent the poker hands thusly:
        straight flush: [8, 14] for highest possible and [8,5] for lowest possible
        4 of Kind: ( four 10's w/ ace kicker ) : [ 7,10,14]
        full house: ( queens full of 9's ) : [ 6,12,9]
        flush : ( flush with king, jack, 9, 6 and a 4 ) : [ 5, 13,11,9,6,4 ]
        straight: (nine high): [ 4,9]
        three of a kind: ( three 6's an Ace and a King ) : [ 3,6,14,13]
        two pair: ( 8'ss and 4's and an ace ) : [ 2,8,4,14]
        pair: ( two 9's, and ace, 10 and a 7 )  : [ 1,14,10,7]
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

    def _matching(self, players):
        """identifies the highest value matching hands eg quads to pairs"""
        for player in players:
            quads = []
            trips = []
            pairs = []
            if not player.hand:
                # create a local variable 'values' to more easily handle the
                # hand.  Easier to deal with a list of values rather than a list
                # of objects
                values = []
                for card in player.hole:
                    values.append(card.value)
                # here we add appropriate values to the quads, trips,
                # and or pairs variables
                for v in values:
                    count = values.count(v)
                    if count == 4:
                        quads = [v]
                        values = [x for x in values if x != v]
                    elif count == 3:
                        trips.append(v)
                        values = [x for x in values if x != v]
                    elif count == 2:
                        pairs.append(v)
                        values = [x for x in values if x != v]
                #Now we create hands based on the quads, trips,
                # and pairs lists.
                if quads:
                    player.hand = [7, quads[0], values[0]]
                elif trips:
                    if len(trips) == 2:
                        player.hand = [6, trips[0], trips[1]]
                    elif pairs:
                        player.hand = [6, trips[0], pairs[0]]
                    else:
                        player.hand = [3, trips[0], values[0], values[1]]
                elif pairs:
                    if len(pairs) > 1:
                        player.hand = [2, pairs[0], pairs[1], values[0]]
                    else:
                        player.hand = [1, pairs[0], values[0], values[1], values[2]]
                else:
                    player.hand = [0, values[0], values[1], values[2], values[3], values[4]]

    def _straight(self, player):
        """identifies the highest straight in a hand"""
            # create a local variable 'values' to more easily handle the
            # hand.  Easier to deal with a list of values rather than a list
            # of objects
        values = []
        for card in player.hole:
            values.append(card.value)
        for v in values:
            if v >= 5 and not player.hand:
                if v - 1 in values and v - 2 in values and v - 3 in values:
                    if v - 4 in values:
                        player.hand = [4, v]
                        break
                    elif v == 5 and 14 in values:
                        player.hand = [4, v]
                        break
        return player

    def _flush(self, players):
        """Identify those hands that are flushes"""
        for player in players:
            suits ={'d': [], 'h': [], 's': [], 'c': []}
            for card in player.hole:
                x = card.suit
                suits[x].append(card)
            for suit in suits:
                if len(suits[suit]) >= 5:
                    player.hole = list(suits[suit])
                    self._straight(player)
                    if player.hand:
                        value = player.hand[1]
                        player.hand = [8, value]
                    else:
                        player.hand = [5] + player.hole
            # if we have a flush only accept the top five cards to make a
            # poker hand
            if player.hand:
                while len(player.hand) > 6:
                    player.hand.pop()
            else:
                self._straight(player)
        return players

    def _order(self, players):
        """order players' hands from highest to lowest"""
        for player in players:
            player.hole.sort(key=lambda x: x.value, reverse=True)
        return players

    def _setup(self):
        """get the players in the pot and their hands"""
        players = []

        """get all active players and append them to players  """

        for seat in self.pot.seats:
            if seat.active:
                players.append(seat.player)

        """ append all all in players to players list"""
        for seat in self.pot.all_in:
            players.append(seat.player)

        for player in players:
            player.hole += self.table.community_cards

        return players

