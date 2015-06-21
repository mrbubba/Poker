from deck import Deck
from table import Table


class Dealer(object):
    """the dealer object wil be responsible for dealing, removing broke players
    from the game and awarding chips to winning players

    Methods:

        new_hand:   removes any player objects from table.seats where
                    player.stack = 0. calls table.init_hand. deals each player
                    in table.players two cards to their player.hole attribute.
                    Then calls pot

        deal:   if there is only one player in the hand adds pot.pot to that
                player.stack. If there is more than one player in the hand and
                less then 5 cards in table.community_cards deals the appropriate
                number of cards. If more then 1 player is in the hand is not all
                in it calls pot.betting_round, else if table.community_cards<5,
                it calls self.deal, else it passes analyzer.analyze the
                community cards, and table.pots
    """

    def __init__(self, table):
        self.table = table
        self.deck = Deck()
        self.deck.create()
        self.players = self.table.players

    def _remove_0_stack(self):
        big_blind = self.players[self.table.big_blind]
        for player in self.players:
            if player.stack == 0:
                if len(self.players) > 3 and player == big_blind:
                    self.table.no_small_blind = True
                    self.players.remove(player)
                else:
                    self.players.remove(player)

    def _deal_hole(self):
        for i in range(0, 2):
            for player in self.players:
                x = self.deck.deal()
                player.hole.append(x)
