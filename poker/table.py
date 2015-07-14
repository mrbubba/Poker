__author__ = 'mark'
import random
from pot import Pot


class Table(object):
    """The table object will largely be the top level object

    Attributes:

        community_cards(list):  a list of the cards shared by all players
        seats(list):  list of seats in the game
        seats_active(int):  number of active seats
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
        # TODO: since the zero's are all indices of lists it might be better to initalize them as None.
        # that way we know that the value has not been actually set.
        self.seats_active = 0
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
        # NOTE: you do not necessarily need to declare active_seat first.
        # e.g.
        # for seat in self.seats:
        #   if seat.active:
        #       try:
        #           active_seat.append(seat)
        #       except NameError:
        #           active_seat = [seat]

        # This is more "pythonic" the advantage is readability and style.

    def set_button(self):
        """At the start of game we need to randomly assign the button
        and blinds to an active seat."""
        self.button = random.randint(1, len(self.seats) - 1)
        self.seats_active = len(Table._get_active_seats(self))

        # check to make sure we've assigned the button to an active seat
        move = True  # Note: you might want to declare this closer to the loop
        # Wouldn't these be false anyway at the start of the game?
        for seat in self.seats:
            if seat.player:
                seat.player.missed_big_blind = False
                seat.player.missed_small_blind = False

        while move:
            if self.seats[self.button].active:
                move = False
            else:
                self.button += 1
                if self.button >= len(self.seats):
                    self.button = 0

        # set the small blind
        self.small_blind = self.button + 1
        move = True
        while move:
            if self.small_blind >= len(self.seats):
                self.small_blind = 0
            if self.seats[self.small_blind].active:
                move = False
            self.small_blind += 1

        # set the big blind
        # NOTE: manicure
        self.big_blind = self.small_blind
        move = True
        while move:
            self.big_blind += 1
            if self.big_blind >= len(self.seats):
                self.big_blind = 0
            if self.seats[self.big_blind].active:
                move = False

        # reset the blinds appropriately for head to head play
        # WARNING! No. you are calling an instance method by referencing the class
        # Better is self._get_active_seats()
        active = Table._get_active_seats(self)
        # QUESTION: since this is a corner case that if it is true could cut off the need
        # for quite a bit of other code should it come earlier?
        if len(active) == 2:
            self.big_blind = self.small_blind
            self.small_blind = self.button

        # NOTE: Mani-pedi at line 106 you are doing the same logic.
        # is there a way to abstract the logic into a method or function?

        # set utg (Under the Gun) for first round of betting (first to act)
        self.under_the_gun = self.big_blind
        move = True
        while move:
            self.under_the_gun += 1
            if self.under_the_gun >= len(self.seats):
                self.under_the_gun = 0
            if self.seats[self.under_the_gun].active:
                move = False

    def _button_move(self):
        """moves the buttons and the blinds"""
        # NOTE: can you be a little more descriptive in the doc string
        # about how the button is supposed to move?
        # exits game when down to a single player
        if self.seats_active == 1:
            quit()
            # WARNING: quit is simply a pass. maybe what you want to do here is
            # raise a custom exception?

        # correctly sets the small blind/button for head to head play
        # WARNING: Programming error seats_active is a list.
        # you should test the length.

        # QUESTION: is there a way to refactor this with the code starting at 119?
        elif self.seats_active == 2:
            self.button = self.big_blind
            self.small_blind = self.big_blind
            move = True
            while move:
                self.big_blind += 1
                if self.big_blind >= len(self.seats):
                    self.big_blind = 0
                if self.seats[self.big_blind].active:
                    move = False

        # if one or more players join on a head to head game reset the button
        elif self.seats_active > 2 and self.button == self.small_blind:
            self.set_button()
        else:
            # ensures that the small blind is moved to the appropriate seat
            move = True
            while move:
                self.small_blind += 1 # NOTE: SFT
                # resets small_blind to 0 if it is greater than seats
                if self.small_blind >= len(self.seats): # REVISIT: we talked about this ... fare catch. Might be a
                                                        # a security issue here.
                    self.small_blind = 0
                # if seat is active ends the loop
                if self.seats[self.small_blind].active:
                    move = False
                elif not self.seats[self.small_blind].player.missed_big_blind:
                    self.seats[self.small_blind].player.missed_small_blind = True
                    move = False
                else:
                    self.seats[self.big_blind].player.missed_small_blind = True

            # ensures that the big blind is moved to the next active seat
            move = True
            while move:
                self.big_blind += 1 # NOTE: SFT
                # resets big_blind to 0 if it is greater than seats
                if self.big_blind >= len(self.seats):
                    self.big_blind = 0
                # if seat is active ends the loop
                if self.seats[self.big_blind].active:
                    self.seats[self.big_blind].missed_big_blind = False
                    self.seats[self.big_blind].missed_small_blind = False
                    move = False
                else:
                    self.seats[self.big_blind].player.missed_big_blind = True
                    self.seats[self.big_blind].player.missed_small_blind = False

            # properly set utg
            move = True
            self.under_the_gun  = self.big_blind
            while move:
                self.under_the_gun += 1
                # resets under_the_gun to 0 if it is greater than seats
                if self.under_the_gun >= len(self.seats):
                    self.under_the_gun = 0
                # if seat is active ends the loop
                if self.seats[self.under_the_gun].active:
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
                    # if ante puts player all in put player in all_in list
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

    def _reset_players(self):
        # set player attributes for start of new hand
        self.community_cards = []
        for seat in self.seats:
            if seat.player is not None:
                seat.player.hole = []
                seat.player.equity = 0

    def _remove_0_stack(self):
        """set seat to inactive for broke players"""
        for seat in self.seats:
            if seat.active and seat.player.stack == 0:
                seat.active = False

    def init_hand(self):
        """sets the table and players up for a new hand, creates a new pot,
        then calls the dealer """

        # How many hands in play
        new_active = len(Table._get_active_seats(self))
        # if we were head to head but have more now... reset the blinds
        if self.seats_active == 2 and new_active > 2:
            Table.set_button(self)

        self.seats_active = new_active
        Table._remove_0_stack(self)
        Table._reset_players(self)
        Table._button_move(self)
        Table._create_pot(self)
        self.dealer.deal_hole()
