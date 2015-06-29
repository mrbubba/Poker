from deck import Deck
from analyzer import Analyzer


class Dealer(object):
    """the dealer object wil be responsible for dealing, removing broke players
    from the game and awarding chips to winning players

    Attributes

        table(obj):  the table object
        deck(obj):  the deck object

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

    def _get_active_players(self):
        """we only want to deal to active players"""
        active_players = []
        for seat in self.table.seats:
            if seat.active:
                active_players.append(seat.player)
        return  active_players

    def deal_hole(self):
        """Deals the two hole cards to all active players"""
        active_players = Dealer._get_active_players(self)
        self.deck.create()
        for i in range(2):
            for player in active_players:
                x = self.deck.deal()
                player.hole.append(x)

    def deal(self):
        pot = self.table.pots(len(self.table.pots)-1)
        first = self.table.seats[self.button + 1]
        if first == len(self.table.seats):
            first = 0
        pot.first = first
        if len(self.table.community_cards) == 0:
            for i in range(3):
                self.table.community_cards.append(self.deck.deal())
                pot.active = True
        elif len(self.table.community_cards) > 2 and len(self.table.community_cards) < 5:
            self.table.community_cards.append(self.deck.deal())
            pot.active = True
        else:
            return Analyzer(self.table)


