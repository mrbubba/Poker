__author__ = 'mark'
import random


class Table(object):
    """The table object will largely be the top level object

    Attributes:

        community_cards(list):  a list of the cards shared by all players
        players(list):  list of players in the game
        old_players(list):  a list of all players in the last hand(for the
                            purpose of moving the blinds)
        button(int):    indicates which player has the button (indicy of player
                        in self.players)
        small_blind_amount(int):  how much the small blind costs
        big_blind_amount(int):  how much the big blind costs
        ante(int):  how much the ante costs
        small_blind(int):  indicates which player has the small blind (indicy
                            of player in self.players)
        big_blind(int):  indicates which player has the big blind (indicy of
                        player in self.players)
        pots(list):  a list of all current pots
        dealer(obj):  the dealer object
        no_small_blind(bool):  Set to True if there is no small blind for the
                                hand.
        no_button_move(bool):  Set to True if the button doesn't move for the
                                hand

    Methods:
         init_hand: moves button to the next player.  Increments the
                    small_blind and big_blind attributes appropriately.  Resets
                    community_cards and pots to [].  Sets all player.hole
                    attributes []. Creates the initial pot object, deducts the
                    blinds and antes and adds them to the pot.pot. Pot inherits
                    the players, and button attributes as well as the
                    big_blind_amount as the initial pot.bet_increment value.
                    Sets old_players = players
    """

    def __init__(self, players, small_blind_amount, big_blind_amount, ante=0):
        self.players = players
        self.small_blind_amount = small_blind_amount
        self.big_blind_amount = big_blind_amount
        self.ante = ante
        self.community_cards = []
        self.oldplayers = players
        self.button = random.randint(1, len(self.players)) - 1
        self.small_blind = 0
        self.big_blind = 0
        self.pots = []
        self.dealer = None
        self.no_small_blind = False

    def _button_move(self):
        self.button += 1
        self.small_blind = self.button + 1
        self.big_blind = self.button + 2
        if self.button >= len(self.players):
            self.button -= len(self.players)
        if len(self.players) == 2:
            self.small_blind = self.button
            self.big_blind = self.button + 1
            if self.big_blind >= len(self.players):
                self.big_blind -= len(self.players)
        else:
            if self.small_blind >= len(self.players):
                self.small_blind -= len(self.players)
            if self.big_blind >= len(self.players):
                self.big_blind -= len(self.players)
