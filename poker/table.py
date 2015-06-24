__author__ = 'mark'
import random
from pot import Pot


class Table(object):
    """The table object will largely be the top level object

    Attributes:

        community_cards(list):  a list of the cards shared by all players
        seats(list):  list of seats in the game
        button(int):    indicates which player has the button (sub of seat
                        in self.seats)
        small_blind_amount(int):  how much the small blind costs
        big_blind_amount(int):  how much the big blind costs
        ante(int):  how much the ante costs
        button(int):  indicates which seat has the button
        small_blind(int):  indicates which seat has the small blind (sub
                            of seat in self.seats)
        big_blind(int):  indicates which player has the big blind (sub of
                        seat in self.seats)
        under_the_gun(int):  first player to act pre-flop
        pots(list):  a list of all current pots
        dealer(obj):  the dealer object

    Methods:

         init_hand: moves button to the next player.  Increments the
                    small_blind and big_blind attributes appropriately.  Resets
                    community_cards and pots to [].  Sets all player.hole
                    attributes []. Creates the initial pot object, deducts the
                    blinds and antes and adds them to the pot.pot. Pot inherits
                    the active seats, and button attributes as well as the
                    big_blind_amount as the initial pot.bet_increment value.
    """

    def __init__(self, seats, small_blind_amount, big_blind_amount, ante=0):
        self.community_cards = []
        self.seats = seats
        self.small_blind_amount = small_blind_amount
        self.big_blind_amount = big_blind_amount
        self.ante = ante
        self.button = 0
        self.small_blind = 0
        self.big_blind = 0
        self.under_the_gun = 0
        self.pots = []
        self.dealer = None

    def _get_active_seats(self):
        active_seat = []
        for seat in self.seats:
            if seat.active:
                active_seat.append(seat)
        return active_seat

    def set_button(self):
        """on start of game we need to randomly assign the button
        and blinds to an active seat"""
        self.button = random.randint(1, len(self.seats) - 1)
        # check to make sure we've assigned the button to an active seat
        button = True
        while button:
            if self.seats[self.button].active:
                button = False
            else:
                self.button += 1
                if self.button >= len(self.seats):
                    self.button = 0

        # set the small blind
        self.small_blind = self.button + 1
        if self.small_blind >= len(self.seats):
            self.small_blind = 0

        # verify that the small blind is active
        sb = True
        while sb:
            if self.seats[self.small_blind].active:
                sb = False
            else:
                self.small_blind += 1
                if self.small_blind >= len(self.seats):
                    self.small_blind = 0

        # set the big blind
        self.big_blind = self.small_blind + 1
        if self.big_blind >= len(self.seats):
            self.big_blind = 0

        # verify that the big blind is active
        bb = True
        while bb:
            if self.seats[self.big_blind].active:
                bb = False
            else:
                self.big_blind += 1
                if self.big_blind >= len(self.seats):
                    self.big_blind = 0

        # reset the blinds appropriately for head to head play
        active = Table._get_active_seats(self)
        if len(active) == 2:
            self.big_blind = self.small_blind
            self.small_blind = self.button

        # set utg (Under the Gun) for first round of betting (first to act)
        self.under_the_gun = self.big_blind + 1
        # verify that the big blind is active
        utg = True
        while utg:
            if self.seats[self.under_the_gun].active:
                utg = False
            else:
                self.under_the_gun += 1
                if self.under_the_gun >= len(self.seats):
                    self.under_the_gun = 0

    def _reset_players(self):
        self.community_cards = []
        for seat in self.seats:
            if seat.player is not None:
                seat.player.hole = []
                seat.player.equity = 0

    def _button_move(self):
        """moves the buttons and the blinds"""
        active = Table._get_active_seats(self)
        # exits game when down to a single player
        if len(active) == 1:
            quit()
        # correctly sets the blinds for head to head play
        elif len(active) == 2:
            self.button = self.big_blind
            self.small_blind = self.big_blind
        else:
            self.button = self.small_blind
            self.small_blind = self.big_blind

        # ensures that the big blind is moved to the next active seat
        move = True
        while move:
            self.big_blind += 1
            if self.big_blind >= len(self.seats):
                self.big_blind = 0
            if self.seats[self.big_blind].active:
                move = False

    def _create_pot(self):
        """creates the initial pot object with the blinds and antes"""
        bb = self.seats[self.big_blind]
        sb = self.seats[self.small_blind]
        all_in = []
        pot = 0
        # if active add the small blind to the pot
        if sb.active:
            if sb.player.stack > self.small_blind_amount:
                sb.player.stack -= self.small_blind_amount
                pot += self.small_blind_amount
                sb.player.equity = self.small_blind_amount
            # if small blind puts player all in put player in all_in list
            elif sb.player.stack <= self.small_blind_amount:
                pot += sb.player.stack
                sb.player.equity = sb.player.stack
                sb.player.stack = 0
                sb.active = False
                all_in.append(sb)

        # add the big blind too the pot
        if bb.player.stack > self.big_blind_amount:
            bb.player.stack -= self.big_blind_amount
            pot += self.big_blind_amount
            bb.player.equity = self.big_blind_amount
            # if big blind puts player all in put player in all_in list
        elif bb.player.stack <= self.big_blind_amount:
            pot += bb.player.stack
            bb.player.equity = bb.player.stack
            bb.player.stack = 0
            bb.active = False
            all_in.append(sb)

        # if there is an ante add it too the pot
        if self.ante is not None:
            active_seats = Table._get_active_seats(self)
            for seat in active_seats:
                if seat.player.stack > self.ante:
                    seat.player.stack -= self.ante
                    pot += self.ante
                else:
                    pot += seat.player.stack
                    seat.player.equity += seat.player.stack
                    seat.player.stack = 0
                    seat.active = False
                    all_in.append(seat)

        new_pot = Pot(pot, self.big_blind_amount, self.big_blind_amount,
                      self.seats, all_in, self.big_blind_amount,
                      self.under_the_gun)
        self.pots = [new_pot]
        return new_pot
