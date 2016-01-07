__author__ = 'mark'
from player import Player
from table import Table
from deck import Card


class AI(object):
    def __init__(self, table, player):
        self.player = player
        self.table = table
        self.cc = self.table.community_cards
        self.hole = self.player.hole
        # merge the community and hole cards
        self.hand = []
        for x in self.cc:
            self.hand.append(x)

        for x in self.hole:
            self.hand.append(x)

        # setup some globals for tricksy hands
        self.quads = []

    def _matching_values(self):

        seen = {}
        for card in self.hand:
            if card.value in seen:
                seen[card.value] += 1
            else:
                seen[card.value] = 1

        return seen

    def _isQuads(self, seen):
        """check for 4 of a kind in hand"""

        for card in seen:
            if seen[card] == 4:
                self.quads = [card]
        # are these board quads? If not then add the Kicker to the self.quad list
        # first, find the highest Kicker
        if self.quads:
            kicker = -1
            for card in self.hand:
                if card.value != self.quads[0] and card.value > kicker:
                    kicker = card.value
            self.quads.append(kicker)
            # Is the Kicker a community card? If so self.quads.append(False) else True
            if len(self.quads) > 1:
                for c in self.table.community_cards:
                    if kicker == c.value and len(self.quads) == 2:
                        self.quads.append(False)
                if len(self.quads) == 2:
                    self.quads.append(True)





