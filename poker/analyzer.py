__author__ = 'mark'
from seat import Seat
from table import Table
from pot import Pot
from player import Player

class Analyzer(object):
    """ Analyzer object

    Attributes:

       table(obj):  table object

    Methods:

        analyze:    gets the community cards and list of pots from the dealer,
                    for each pot awards the chips to the winner/s
                    If an all in player wins, analyze will reset that seats
                    active to True
    """

    def __init__(self, table):
        self.table = table

    def _setup(self, pot):
        """get the players in the pot and their hands"""
        pot = pot
        players = []

        """ yes this appending is correct """
        for seat in pot.seats:
            players.append(seat.player)

        """ yes this appending is correct ( because players have been removed from pot.seats if all_in"""
        for seat in pot.all_in:
            players.append(seat.player)

        for player in players:
            player.hole.append(self.table.community_cards)

        return players

